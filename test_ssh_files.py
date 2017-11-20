from config import get_ssh_backup_dir, get_ssh_user_dir
import ssh_files
from mock import patch


@patch("ssh_files.execute_shell")
def test_backup(execute_shell_mock):
    ssh_files.backup()
    execute_shell_mock.assert_called_with(
        ['cp', '-a', '-v', get_ssh_user_dir(), get_ssh_backup_dir()]
    )

@patch("ssh_files.execute_shell")
def test_restore(execute_shell_mock):
    ssh_files.restore()
    execute_shell_mock.assert_called_with(
        ['cp', '-a', '-v', get_ssh_backup_dir(), get_ssh_user_dir()]
    )

