from os import path
from mock import patch
import preferences
from config import get_preferences_backup_dir


@patch("preferences.execute_shell")
def test_backup(execute_shell_mock):
    execute_shell_mock.side_effect = execute_shell_func
    preferences.backup()


def execute_shell_func(*args):
    command = args[0]
    if command[1] == "domains":
        return domains_func(command)
    if command[1] == "export":
        return exports_func(command)
    if command[1] == "import":
        return imports_func(command)


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
    backup_dir = get_preferences_backup_dir()
    global_file = path.join(backup_dir, "NSGlobalDomain.plist")
    asdf_file = path.join(backup_dir, "asdf.com.plist")
    assert global_file in command[3] or asdf_file in command[3]

@patch("preferences.get_domains")
@patch("preferences.execute_shell")
def test_restore(execute_shell_mock, get_domains_mock):
    execute_shell_mock.side_effect = execute_shell_func
    get_domains_mock.side_effect = get_domains
    preferences.restore()

def get_domains():
    return ['asdf.com']

def imports_func(*args):
    command = args[0]
    backup_dir = get_preferences_backup_dir()
    assert isinstance(command, list)
    assert len(command) == 4
    assert command[0] == "defaults"
    assert command[1] == "import"
    assert command[2] == "asdf.com"
    assert command[3] == path.join(backup_dir, "asdf.com.plist")

@patch("os.listdir")
def test_get_domains(listdir_mock):
    listdir_mock.side_effect = listdir_func
    result = preferences.get_domains()
    assert result[0] == "asdf.com"

#pylint: disable=unused-argument
def listdir_func(directory):
    return ['asdf.com.plist']