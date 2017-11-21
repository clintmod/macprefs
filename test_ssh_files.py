from config import get_ssh_backup_dir, get_ssh_user_dir
import ssh_files
from mock import patch


@patch("ssh_files.copy_files")
def test_backup(copy_files_mock):
    ssh_files.backup()
    copy_files_mock.assert_called_with(
        get_ssh_user_dir(), get_ssh_backup_dir()
    )

@patch("ssh_files.copy_files")
def test_restore(copy_files_mock):
    ssh_files.restore()
    copy_files_mock.assert_called_with(
        get_ssh_backup_dir(), get_ssh_user_dir()
    )
