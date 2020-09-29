from io import StringIO
import sys
import logging as log
from mock import patch, MagicMock

import utils

# load as module
macprefs = utils.execute_module('macprefs', 'macprefs')

@patch('sys.stdout', new_callable=StringIO)
def test_invoke_help(mock_stdout):
    try:
        sys.argv = ['macprefs', '-h']
        # invoke as script
        utils.execute_module('__main__', 'macprefs')
        assert False, 'expected SystemExit'
    except SystemExit as e:
        assert_correct_std_out(e, mock_stdout)


@patch('macprefs.invoke_func')
def test_main_invokes_backup(invoke_func_mock):
    sys.argv = ['macprefs', 'backup']
    macprefs.main()
    # pylint: disable=unused-variable
    args, kwargs = invoke_func_mock.call_args
    assert args[0].func == macprefs.backup


@patch('macprefs.invoke_func')
def test_main_invokes_restore(invoke_func_mock):
    sys.argv = ['macprefs', 'restore']
    macprefs.main()
    # pylint: disable=unused-variable
    args, kwargs = invoke_func_mock.call_args
    assert args[0].func == macprefs.restore


def test_invoke_func():
    mock = MagicMock()
    macprefs.invoke_func(mock)
    mock.func.assert_called_once()


@patch('sys.stdout', new_callable=StringIO)
def test_invoke_no_args(mock_stdout):
    try:
        sys.argv = ['macprefs']
        # invoke as script
        utils.execute_module('__main__', 'macprefs')
        assert False, 'expected SystemExit'
    except SystemExit as e:
        assert_correct_std_out(e, mock_stdout)

@patch('internet_accounts.backup')
@patch('app_store_preferences.backup')
@patch('startup_items.backup')
@patch('ssh_files.backup')
@patch('dotfiles.backup')
@patch('shared_file_lists.backup')
@patch('system_preferences.backup')
@patch('preferences.backup')
# pylint: disable-msg=too-many-arguments
def test_backup(system_preferences_mock, preferences_mock,
                shared_files_mock, dotfiles_mock,
                ssh_mock, startup_mock, app_store_mock,internet_accounts_mock):
    macprefs.backup()
    system_preferences_mock.assert_called_once()
    preferences_mock.assert_called_once()
    shared_files_mock.assert_called_once()
    dotfiles_mock.assert_called_once()
    ssh_mock.assert_called_once()
    startup_mock.assert_called_once()
    app_store_mock.assert_called_once()
    internet_accounts_mock.assert_called_once()

@patch('internet_accounts.restore')
@patch('app_store_preferences.restore')
@patch('startup_items.restore')
@patch('ssh_files.restore')
@patch('dotfiles.restore')
@patch('shared_file_lists.restore')
@patch('system_preferences.restore')
@patch('preferences.restore')
# pylint: disable-msg=too-many-arguments
def test_restore(system_preferences_mock, preferences_mock,
                 shared_files_mock, dotfiles_mock,
                 ssh_mock, startup_mock, app_store_mock,internet_accounts_mock):
    macprefs.restore()
    system_preferences_mock.assert_called_once()
    preferences_mock.assert_called_once()
    shared_files_mock.assert_called_once()
    dotfiles_mock.assert_called_once()
    ssh_mock.assert_called_once()
    startup_mock.assert_called_once()
    app_store_mock.assert_called_once()
    internet_accounts_mock.assert_called_once()


def assert_correct_std_out(e, mock_stdout):
    assert e.code == 0
    assert 'usage: macprefs' in mock_stdout.getvalue()
    assert 'backup preferences' in mock_stdout.getvalue()
    assert 'restore preferences' in mock_stdout.getvalue()
    assert 'show this help message and exit' in mock_stdout.getvalue()

@patch('macprefs.log.basicConfig')
def test_configure_logging(config_mock):
    macprefs.configure_logging(0)
    config_mock.assert_called_with(
        format="%(message)s", level=log.INFO
    )

@patch('macprefs.log.basicConfig')
def test_configure_logging_works_with_verbose(config_mock):
    macprefs.configure_logging(1)
    config_mock.assert_called_with(
        format="%(message)s", level=log.DEBUG
    )


# pylint: disable=pointless-string-statement
''' @pytest.mark.integration
def test_intergration():
    try:
        sys.argv = ['macprefs', 'backup']
        # invoke as script
        utils.execute_module('__main__', 'macprefs')
        assert False, 'expected SystemExit'
    except SystemExit as e:
        assert e.code == 0


@pytest.mark.integration
def test_restore_intergration():
    try:
        sys.argv = ['macprefs', 'restore']
        # invoke as script
        utils.execute_module('__main__', 'macprefs')
        assert False, 'expected SystemExit'
    except SystemExit as e:
        assert e.code == 0 '''
