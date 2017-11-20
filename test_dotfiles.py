import dotfiles
from mock import patch
from config import get_dotfiles_backup_dir, get_home_dir


@patch('utils.check_output')
def test_backup(check_output_mock):
    dotfiles.backup()
    # pylint: disable=unused-variable
    args, kwargs = check_output_mock.call_args
    command = args[0]
    assert command[0] == 'cp'
    assert command[1] == '-a'
    assert command[-1] == get_dotfiles_backup_dir()
    assert command[-1][-1] == '/'


@patch('utils.check_output')
def test_restore(check_output_mock):
    dotfiles.restore()
    # pylint: disable=unused-variable
    args, kwargs = check_output_mock.call_args
    command = args[0]
    assert command[0] == 'cp'
    assert command[1] == '-a'
    assert command[-1] == get_home_dir()
    assert command[-1][-1] == '/'
