from StringIO import StringIO
import imp
import sys
from mock import patch
import pytest


# load as module should work
macprefs = imp.load_source('macprefs', 'macprefs')


@patch('sys.stdout', new_callable=StringIO)
def test_invoke_help(mock_stdout):
    try:
        sys.argv = ['macprefs', '-h']
        # invoke as script
        imp.load_source('__main__', 'macprefs')
    except SystemExit as e:
        assert_correct_std_out(e, mock_stdout)


@patch('sys.stdout', new_callable=StringIO)
def test_invoke_no_args(mock_stdout):
    try:
        sys.argv = ['macprefs']
        # invoke as script
        imp.load_source('__main__', 'macprefs')
    except SystemExit as e:
        assert_correct_std_out(e, mock_stdout)


def assert_correct_std_out(e, mock_stdout):
    assert e.code == 0
    assert 'usage: macprefs' in mock_stdout.getvalue()
    assert 'Backup mac preferences' in mock_stdout.getvalue()
    assert 'Restore mac preferences' in mock_stdout.getvalue()
    assert 'show this help message and exit' in mock_stdout.getvalue()


@patch('backup_system_preferences.backup')
@patch('backup_preferences.backup')
def test_backup(backup_system_preferences_mock, backup_preferences_mock):
    macprefs.backup()
    backup_system_preferences_mock.assert_called_once()
    backup_preferences_mock.assert_called_once()


@patch('restore_system_preferences.restore')
@patch('restore_preferences.restore')
def test_restore(restore_system_preferences_mock, restore_preferences_mock):
    macprefs.restore()
    restore_system_preferences_mock.assert_called_once()
    restore_preferences_mock.assert_called_once()


@pytest.mark.integration
def test_backup_intergration():
    try:
        sys.argv = ['macprefs', 'backup']
        # invoke as script
        imp.load_source('__main__', 'macprefs')
    except SystemExit as e:
        assert e.code == 0


@pytest.mark.integration
def test_restore_intergration():
    try:
        sys.argv = ['macprefs', 'restore']
        # invoke as script
        imp.load_source('__main__', 'macprefs')
    except SystemExit as e:
        assert e.code == 0
