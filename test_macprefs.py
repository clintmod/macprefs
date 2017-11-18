from StringIO import StringIO
import imp
import sys
from mock import patch
#import pytest


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

@patch('shared_file_lists.backup')
@patch('system_preferences.backup')
@patch('preferences.backup')
def test_backup(system_preferences_mock, preferences_mock, shared_files_mock):
    macprefs.backup()
    system_preferences_mock.assert_called_once()
    preferences_mock.assert_called_once()
    shared_files_mock.assert_called_once()

@patch('shared_file_lists.restore')
@patch('system_preferences.restore')
@patch('preferences.restore')
def test_restore(system_preferences_mock, preferences_mock, shared_files_mock):
    macprefs.restore()
    system_preferences_mock.assert_called_once()
    preferences_mock.assert_called_once()
    shared_files_mock.assert_called_once()


''' @pytest.mark.integration
def test_intergration():
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
        assert e.code == 0 '''
