from os import path
from mock import patch

import backup_preferences
from config import get_backup_dir


@patch("backup_preferences.execute_shell")
def test_backup(execute_shell_mock):
    execute_shell_mock.side_effect = execute_shell_func
    backup_preferences.backup()


def execute_shell_func(*args):
    command = args[0]
    if command[1] == "domains":
        return domains_func(command)
    if command[1] == "export":
        return exports_func(command)


def domains_func(command):
    assert isinstance(command, list)
    assert len(command) == 2
    assert command[0] == "defaults"
    assert command[1] == "domains"
    return ", ".join(["asdf.com"])


def exports_func(command):
    assert isinstance(command, list)
    assert len(command) == 4
    assert command[0] == "defaults"
    assert command[1] == "export"
    assert "NSGlobalDomain" in command[2] or "asdf.com" in command[2]
    backup_dir = get_backup_dir()
    nsgd_file = path.join(backup_dir, "/NSGlobalDomain.plist")
    asdf_file = path.join(backup_dir, "asdf.com.plist")
    assert nsgd_file in command[3] or asdf_file in command[3]
