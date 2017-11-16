from StringIO import StringIO
import restore_system_preferences
from mock import patch

@patch("restore_system_preferences.execute_shell")
@patch("os.getuid")
def test_restore_works_if_sudo(get_uid_mock, execute_shell_mock):
    execute_shell_mock.side_effect = execute_shell_func
    get_uid_mock.side_effect = get_uid_func
    restore_system_preferences.power_management_restore_path = "pmrp"
    restore_system_preferences.power_management_domain = "pmd"
    restore_system_preferences.restore()

@patch('sys.stdout', new_callable=StringIO)
def test_restore_exits_if_not_sudo(mock_stdout):
    try:
        restore_system_preferences.restore()
    except SystemExit as e:
        assert_correct_std_out(e, mock_stdout)

def execute_shell_func(*args):
    arg_length = len(args)
    assert  arg_length > 0
    command = args[0]
    assert command[0] == "defaults"
    assert command[1] == "import"
    assert command[2] == "pmd"
    assert command[3] == "pmrp"

def get_uid_func():
    return 0

def assert_correct_std_out(e, mock_stdout):
    assert e.code == 1
    assert 'sudo is required' in mock_stdout.getvalue()