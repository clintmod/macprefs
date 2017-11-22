import system_preferences
from mock import patch


@patch("system_preferences.execute_shell")
def test_backup(execute_shell_mock):
    domain = system_preferences.get_domain()
    pm_file = system_preferences.get_pm_backup_path()
    system_preferences.backup()
    execute_shell_mock.assert_called_with(['defaults', 'export', domain, pm_file])


@patch("system_preferences.execute_shell")
def test_restore(execute_shell_mock):
    domain = system_preferences.get_domain()
    pm_file = system_preferences.get_pm_backup_path()
    system_preferences.restore()
    execute_shell_mock.assert_called_with(['sudo', 'bash', '-c', 'defaults import ' + domain + ' ' + pm_file])


@patch("system_preferences.path.exists")
def test_get_domain(exists_mock):
    exists_mock.return_value = False
    result = system_preferences.get_domain()
    assert "SystemConfiguration" in result
