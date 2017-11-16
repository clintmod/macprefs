from os import path
from mock import patch

import config
import restore_preferences


@patch("restore_preferences.get_domains")
@patch("restore_preferences.execute_shell")
def test_restore(execute_shell_mock, get_domains_mock):
    execute_shell_mock.side_effect = execute_shell_func
    get_domains_mock.side_effect = get_domains
    restore_preferences.restore()


@patch("os.listdir")
def test_get_domains(listdir_mock):
    listdir_mock.side_effect = listdir_func
    result = restore_preferences.get_domains()
    assert result[0] == "asdf.com"

#pylint: disable=unused-argument
def listdir_func(directory):
    return ['asdf.com.plist']


def execute_shell_func(*args):
    command = args[0]
    backup_dir = config.get_backup_dir()
    assert isinstance(command, list)
    assert len(command) == 4
    assert command[0] == "defaults"
    assert command[1] == "import"
    assert command[2] == "asdf.com"
    assert command[3] == path.join(backup_dir, "asdf.com.plist")


def get_domains():
    return ["asdf.com"]
