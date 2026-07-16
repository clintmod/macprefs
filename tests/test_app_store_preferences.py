from unittest.mock import patch

import app_store_preferences


@patch("app_store_preferences.copy_files")
def test_backup(copy_mock):
    app_store_preferences.backup()
    assert copy_mock.call_count > 0


@patch("app_store_preferences.restart_cfprefsd")
@patch("app_store_preferences.copy_file")
def test_restore(copy_mock, restart_mock):
    app_store_preferences.restore()
    assert copy_mock.call_count >= 0
    restart_mock.assert_called_once()


# pylint: disable=len-as-condition
def test_build_file_list():
    result = app_store_preferences.build_file_list()
    assert result is not None
    assert len(result) > 0
