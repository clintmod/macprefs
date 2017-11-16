from subprocess import CalledProcessError
import utils
from mock import patch


@patch('utils.check_output')
def test_execute_shell(check_output_mock):
    check_output_mock.side_effect = check_output_func
    utils.execute_shell(['wtf'])

# pylint: disable=unused-argument


def check_output_func(command, shell, cwd, stderr):
    length = len(command)
    assert length > 0
    assert command[0] == 'wtf'
    return ""


@patch('utils.check_output')
def test_execute_shell_handles_errors(check_output_mock):
    check_output_mock.side_effect = check_output_error_func
    try:
        utils.execute_shell(['expecting error'])
    except CalledProcessError:
        pass


def check_output_error_func(command, shell, cwd, stderr):
    raise CalledProcessError(0, command)


@patch('utils.check_output')
def test_execute_shell_handles_verbose(check_output_mock):
    utils.execute_shell(['wtf'], False, ".", False, True)
