from os import path
from mock import patch

import dotfiles
from config import get_dotfiles_backup_dir, get_home_dir, get_user

@patch('dotfiles.get_dot_files')
@patch('dotfiles.copy_files')
def test_backup(copy_files_mock, dotfiles_mock):
    files = ['.no_file']
    dotfiles_mock.return_value = files
    dotfiles.backup()
    dest = get_dotfiles_backup_dir()
    copy_files_mock.assert_called_with(
        files, dest
    )


@patch('dotfiles.ensure_files_owned_by_user')
@patch('dotfiles.get_dot_files')
@patch('dotfiles.copy_files')
def test_restore(copy_files_mock, dotfiles_mock, ensure_mock):
    files = ['.no_file']
    dest = get_home_dir()
    dotfiles_mock.return_value = files
    dotfiles.restore()
    copy_files_mock.assert_called_with(
        files, dest
    )
    ensure_mock.assert_called_with(
        get_user(), files
    )

@patch('dotfiles.path.isfile')
@patch('dotfiles.listdir')
def test_get_dot_files(listdir_mock, isfile_mock):
    files = ['testfile', '.no_file', '.good_file']
    listdir_mock.return_value = files
    isfile_mock.return_value = True
    home_dir = get_home_dir()
    result = dotfiles.get_dot_files(home_dir)
    assert result[0] == path.join(home_dir, files[1])
