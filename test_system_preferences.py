from os import path
from mock import patch

import system_preferences
from config import get_sys_preferences_backup_dir

@patch('system_preferences.copy_dir')
def test_backup(copy_dir_mock):
    source = system_preferences.get_pm_path()
    dest = system_preferences.get_pm_backup_path()
    system_preferences.backup()
    copy_dir_mock.assert_called_with(
        source, dest
    )

@patch('system_preferences.ensure_files_owned_by_user')
@patch('system_preferences.copy_dir')
def test_restore(copy_dir_mock, ensure_mock):
    source = system_preferences.get_pm_backup_path()
    dest = system_preferences.get_pm_path()
    system_preferences.restore()
    copy_dir_mock.assert_called_with(
        source, dest, with_sudo=True
    )
    ensure_mock.assert_called_with(
        'root:wheel', [dest], '644'
    )

def test_get_pm_backup_path():
    result = system_preferences.get_pm_backup_path()
    assert result == path.join(get_sys_preferences_backup_dir(), system_preferences.pm_file_name)

@patch('system_preferences.path.exists')
def test_get_pm_path(exists_mock):
    exists_mock.return_value = False
    result = system_preferences.get_pm_path()
    assert 'SystemConfiguration' in result
