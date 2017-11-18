from mock import patch
import shared_file_lists


@patch("shared_file_lists.execute_shell")
def test_backup_works(execute_shell_mock):
    execute_shell_mock.side_effect = execute_shell_func
    shared_file_lists.backup()

@patch("shared_file_lists.execute_shell")
def test_restore_works(execute_shell_mock):
    execute_shell_mock.side_effect = execute_shell_func
    shared_file_lists.restore()


def execute_shell_func(*args):
    command = args[0]
    assert command[0] == "cp"
    assert command[1] == "-r"
    # ensure trailing slashes in src and dest
    assert command[2][-1] == "/"
    assert command[3][-1] == "/"
    return ""