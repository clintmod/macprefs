from config import get_ssh_backup_dir, get_ssh_user_dir, get_user
import ssh_files
from mock import patch


@patch("ssh_files.copy_files")
def test_backup(copy_files_mock):
    ssh_files.backup()
    copy_files_mock.assert_called_with(
        get_ssh_user_dir(), get_ssh_backup_dir()
    )
@patch("ssh_files.ensure_owned_by_user")
@patch("ssh_files.copy_files")
def test_restore(copy_files_mock, ensure_mock):
    dest = get_ssh_user_dir()
    ssh_files.restore()
    copy_files_mock.assert_called_with(
        get_ssh_backup_dir(), dest,
        as_archive=False, as_dir=True, with_sudo=True
    )
    ensure_mock.assert_called_with(dest, get_user())
