from StringIO import StringIO
import system_preferences
from mock import patch


@patch("system_preferences.execute_shell")
def test_backup(execute_shell_mock):
    execute_shell_mock.side_effect = execute_shell_func
    system_preferences.backup()


def execute_shell_func(*args):
    command = args[0]
    if command[1] == "export":
        return exports_func(command)
    if command[1] == "import":
        return imports_func(command)


def exports_func(args):
    arg_length = len(args)
    assert arg_length > 0
    assert args[0] == "defaults"
    assert args[1] == "export"

@patch("system_preferences.get_pm_file_path")
@patch("system_preferences.execute_shell")
@patch("os.getuid")
def test_restore_works_if_sudo(get_uid_mock, execute_shell_mock, get_pm_file_path_mock):
    execute_shell_mock.side_effect = execute_shell_func
    get_uid_mock.side_effect = get_uid_func
    get_pm_file_path_mock.side_effect = get_pm_file_path_func
    system_preferences.restore()

def get_pm_file_path_func():
    return 'asdf.plist'

@patch('sys.stdout', new_callable=StringIO)
def test_restore_exits_if_not_sudo(mock_stdout):
    try:
        system_preferences.restore()
    except SystemExit as e:
        assert_correct_std_out(e, mock_stdout)


def imports_func(*args):
    arg_length = len(args)
    assert arg_length > 0
    command = args[0]
    assert command[0] == "defaults"
    assert command[1] == "import"
    assert command[2] == "asdf"
    assert command[3] == "asdf.plist"


def get_uid_func():
    return 0


def assert_correct_std_out(e, mock_stdout):
    assert e.code == 1
    assert 'sudo is required' in mock_stdout.getvalue()

@patch("system_preferences.path.exists")
def test_get_pm_path(exists_mock):
    exists_mock.return_value = False
    result = system_preferences.get_pm_file_path()
    assert "SystemConfiguration" in result
