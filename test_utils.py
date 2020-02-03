from subprocess import CalledProcessError
import logging as log
from mock import patch

import utils
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
    return b''


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

@patch('utils.log.root.getEffectiveLevel')
@patch('utils.execute_shell')
def test_copy_dir(execute_shell_mock, level_mock):
    level_mock.return_value = log.DEBUG
    utils.copy_dir('src', 'dest')
    execute_shell_mock.assert_called_with(
        ['rsync', '-a', '-vv', 'src', 'dest']
    )


@patch('utils.execute_shell')
def test_copy_dir_works_with_sudo(execute_shell_mock):
    utils.copy_dir('src', 'dest', with_sudo=True)
    execute_shell_mock.assert_called_with(
        ['sudo', 'rsync', '-a', 'src', 'dest']
    )

@patch('utils.log.root.getEffectiveLevel')
@patch('utils.execute_shell')
def test_copy_files(execute_shell_mock, log_mock):
    log_mock.return_value = log.DEBUG
    files = ['asdf']
    dest = "asdf2"
    utils.copy_files(files, dest)
    print(log_mock.mock_calls)
    execute_shell_mock.assert_called_with(
        ['rsync', '-a', '-vv'] + files + [dest]
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


@patch('utils.ensure_subdirs_listable')
@patch('utils.change_owner')
@patch('utils.change_mode')
def test_ensure_dir_owned_by_user(chmod_mock, chown_mock, listable_mock):
    dest = config.get_ssh_user_dir
    utils.ensure_dir_owned_by_user(dest, 'clint')
    chmod_mock.assert_called_with(dest, '600')
    chown_mock.assert_called_with(dest, 'clint')
    listable_mock.assert_called_with(dest)


@patch('utils.change_owner_for_files')
@patch('utils.change_mode_for_files')
def test_ensure_files_owned_by_user(mode_mock, owner_mock):
    files = ['.no_file']
    mode = '622'
    user = config.get_user()
    utils.ensure_files_owned_by_user(user, files, mode)
    mode_mock.assert_called_with(files, mode)
    owner_mock.assert_called_with(files, user)


@patch('utils.execute_shell')
def test_change_owner_for_files(shell_mock):
    files = ['.no_file']
    user = config.get_user()
    utils.change_owner_for_files(files, user)
    shell_mock.assert_called_with(
        ['sudo', 'chown', user] + files
    )


@patch('utils.execute_shell')
def test_change_mode_for_files(shell_mock):
    files = ['.no_file']
    mode = '622'
    utils.change_mode_for_files(files, mode)
    shell_mock.assert_called_with(
        ['sudo', 'chmod', mode] + files
    )


def test_is_none_or_empty_string():
    assert utils.is_none_or_empty_string('')
    assert utils.is_none_or_empty_string(None)
    assert not utils.is_none_or_empty_string('asdf')

@patch('utils.log.root.getEffectiveLevel')
@patch("utils.execute_shell")
def test_copy_file(shell_mock, level_mock):
    level_mock.return_value = log.DEBUG
    fle = "asdf"
    dest = "wtf"
    utils.copy_file(fle, dest)
    shell_mock.assert_called_with(
        ['rsync', '-a', '-vv', fle, dest]
    )
