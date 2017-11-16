import backup_system_preferences
from mock import patch


@patch("backup_system_preferences.execute_shell")
def test_backup(execute_shell_mock):
    execute_shell_mock.side_effect = execute_shell_func
    backup_system_preferences.backup()


def execute_shell_func(*args):
    arg_length = len(args)
    assert arg_length > 0
    command = args[0]
    assert command[0] == "defaults"
    assert command[1] == "export"
