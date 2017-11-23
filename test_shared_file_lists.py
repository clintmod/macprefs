from mock import patch
import shared_file_lists
import config


@patch("shared_file_lists.copy_files")
def test_backup_works(copy_files_mock):
    shared_file_lists.backup()
    copy_files_mock.assert_called_with(
        config.get_shared_file_lists_dir(),
        config.get_shared_file_lists_backup_dir()
    )


@patch("shared_file_lists.ensure_dir_owned_by_user")
@patch("shared_file_lists.copy_files")
def test_restore_works(copy_files_mock, owned_mock):
    shared_file_lists.restore()
    copy_files_mock.assert_called_with(
        config.get_shared_file_lists_backup_dir(),
        config.get_shared_file_lists_dir(), with_sudo=True
    )
    owned_mock.assert_called_with(config.get_shared_file_lists_dir(), config.get_user())