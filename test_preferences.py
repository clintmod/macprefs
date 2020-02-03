from mock import patch
from config import get_preferences_dir, get_preferences_backup_dir, get_user
import preferences


@patch('preferences.copy_dir')
def test_backup(copy_dir_mock):
    source = get_preferences_dir()
    dest = get_preferences_backup_dir()
    preferences.backup()
    copy_dir_mock.assert_called_with(
        source, dest
    )

@patch('preferences.ensure_dir_owned_by_user')
@patch('preferences.copy_dir')
def test_restore(copy_dir_mock, ensure_mock):
    source = get_preferences_backup_dir()
    dest = get_preferences_dir()
    preferences.restore()
    copy_dir_mock.assert_called_with(
        source, dest, with_sudo=True
    )
    ensure_mock.assert_called_with(
        dest, get_user()
    )