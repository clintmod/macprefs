from os import path
import dotfiles
from mock import patch
from config import get_dotfiles_backup_dir, get_home_dir, get_user

@patch('dotfiles.get_dot_files')
@patch('dotfiles.execute_shell')
def test_backup(execute_shell_mock, dotfiles_mock):
    files = ['.no_file']
    dotfiles_mock.return_value = files
    dotfiles.backup()
    dest = get_dotfiles_backup_dir()
    execute_shell_mock.assert_called_with(
        ['cp', '-a', '-v'] + files + [dest]
    )


@patch('dotfiles.ensure_files_owned_by_user')
@patch('dotfiles.get_dot_files')
@patch('dotfiles.execute_shell')
def test_restore(execute_shell_mock, dotfiles_mock, ensure_mock):
    files = ['.no_file']
    dotfiles_mock.return_value = files
    dotfiles.restore()
    ensure_mock.assert_called_with(
        get_user(), files
    )
    dest = get_home_dir()
    execute_shell_mock.assert_called_with(
        ['sudo', 'cp', '-a', '-v'] + files + [dest]
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
