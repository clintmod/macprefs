from subprocess import CalledProcessError
import utils
from mock import patch
import config


@patch('utils.check_output')
def test_execute_shell(check_output_mock):
    check_output_mock.side_effect = check_output_func
    utils.execute_shell(['asdf'])


# pylint: disable=unused-argument
def check_output_func(command, shell, cwd, stderr):
    length = len(command)
    assert length > 0
    assert command[0] == 'asdf'
    return ""


@patch('utils.check_output')
def test_execute_shell_handles_errors(check_output_mock):
    check_output_mock.side_effect = check_output_error_func
    try:
        utils.execute_shell(['expecting error'])
        assert False, 'expected CalledProcessError'
    except CalledProcessError:
        pass


def check_output_error_func(command, shell, cwd, stderr):
    raise CalledProcessError(0, command)


@patch('utils.check_output')
def test_execute_shell_handles_verbose(check_output_mock):
    utils.execute_shell(['asdf'], False, ".", False, True)


@patch('utils.execute_shell')
def test_copy_files_works_with_extra_args(execute_shell_mock):
    utils.copy_files('src', 'dest', as_archive=True, extra_args=['wtf'])
    execute_shell_mock.assert_called_with(
        ['cp', '-a', '-v', 'wtf', 'src', 'dest']
    )


@patch('utils.execute_shell')
def test_copy_files(execute_shell_mock):
    utils.copy_files('src', 'dest', as_archive=True, as_dir=True)
    execute_shell_mock.assert_called_with(
        ['cp', '-a', '-v', '-r', 'src', 'dest']
    )


@patch('utils.execute_shell')
def test_copy_files_works_with_sudo(execute_shell_mock):
    utils.copy_files('src', 'dest', as_archive=True, with_sudo=True)
    execute_shell_mock.assert_called_with(
        ['sudo', 'cp', '-a', '-v', 'src', 'dest']
    )

@patch('utils.execute_shell')
def test_change_owner(execute_shell_mock):
    ssh_dir = config.get_ssh_user_dir()
    utils.change_owner(ssh_dir, 'clint', True)
    execute_shell_mock.assert_called_with(
        ['sudo', 'chown', '-R', 'clint', ssh_dir]
    )


@patch('utils.execute_shell')
def test_change_mode(execute_shell_mock):
    ssh_dir = config.get_ssh_user_dir()
    utils.change_mode(ssh_dir, 600, True)
    execute_shell_mock.assert_called_with(
        ['sudo', 'chmod', '-R', '600', ssh_dir]
    )


@patch('utils.execute_shell')
def test_ensure_subdirs_listable(execute_shell_mock):
    ssh_dir = config.get_ssh_user_dir()
    utils.ensure_subdirs_listable(config.get_ssh_user_dir())
    execute_shell_mock.assert_called_with(
        ['sudo', 'chmod', '-R', 'a+X', ssh_dir]
    )


@patch("utils.ensure_subdirs_listable")
@patch("utils.change_owner")
@patch("utils.change_mode")
def test_ensure_owned_by_user(chmod_mock, chown_mock, listable_mock):
    dest = config.get_ssh_user_dir
    utils.ensure_owned_by_user(dest, 'clint')
    chmod_mock.assert_called_with(dest, '600')
    chown_mock.assert_called_with(dest, 'clint')
    listable_mock.assert_called_with(dest)