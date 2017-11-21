from subprocess import CalledProcessError
import utils
from mock import patch


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


def test_execute_shell_raises_error_if_cp_is_called_with_dash_a():
    try:
        utils.execute_shell(['cp'])
        assert False, 'expected ValueError'
    except ValueError as e:
        assert 'cp requires -a' in e.message


@patch('utils.execute_shell')
def test_copy_files_works_with_extra_args(execute_shell_mock):
    utils.copy_files('src', 'dest', ['wtf'])
    execute_shell_mock.assert_called_with(
        ['cp', '-a', '-v', 'wtf', 'src', 'dest']
    )


@patch('utils.execute_shell')
def test_copy_files(execute_shell_mock):
    utils.copy_files('src', 'dest')
    execute_shell_mock.assert_called_with(
        ['cp', '-a', '-v', 'src', 'dest']
    )
