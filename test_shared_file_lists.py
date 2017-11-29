from mock import patch
import shared_file_lists
import config


@patch('shared_file_lists.copy_dir')
def test_backup_works(copy_dir_mock):
    shared_file_lists.backup()
    copy_dir_mock.assert_called_with(
        config.get_shared_file_lists_dir(),
        config.get_shared_file_lists_backup_dir()
    )


@patch('shared_file_lists.exists')
@patch('shared_file_lists.copy_dir')
def test_backup_warns_if_not_exists(copy_dir_mock, exists_mock):
    exists_mock.return_value = False
    shared_file_lists.backup()
    copy_dir_mock.assert_not_called()



@patch('shared_file_lists.ensure_dir_owned_by_user')
@patch('shared_file_lists.copy_dir')
def test_restore_works(copy_dir_mock, owned_mock):
    shared_file_lists.restore()
    copy_dir_mock.assert_called_with(
        config.get_shared_file_lists_backup_dir(),
        config.get_shared_file_lists_dir(), with_sudo=True
    )
    owned_mock.assert_called_with(config.get_shared_file_lists_dir(), config.get_user())