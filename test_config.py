import os
from os import path
from mock import patch

import config

def test_get_macprefs_dir():
    backup_dir = config.get_macprefs_dir()
    assert backup_dir is not None


@patch('config.makedirs')
# pylint: disable=unused-argument
def test_get_macprefs_dir_works_with_environ(makedirs_mock):
    os.environ['MACPREFS_BACKUP_DIR'] = 'asdf'
    backup_dir = config.get_macprefs_dir()
    del os.environ['MACPREFS_BACKUP_DIR']
    assert 'asdf' in backup_dir


@patch('config.path.exists')
@patch('config.makedirs')
def test_get_macprefs_dir_creates_if_not_exists(exists_mock, makedirs_mock):
    exists_mock.return_value = False
    config.get_macprefs_dir()
    makedirs_mock.assert_called_once()


def test_get_preferences_dir():
    assert config.get_preferences_dir() == path.join(
        config.get_home_dir(), 'Library/Preferences/')


def test_get_ssh_backup_dir():
    assert config.get_ssh_backup_dir() == path.join(
        config.get_macprefs_dir(), 'ssh/')


def test_get_ssh_user_dir():
    assert config.get_ssh_user_dir() == path.join(
        config.get_home_dir(), '.ssh/')


def test_get_shared_file_lists_dir():
    path.join(config.get_home_dir(), 'Library/Application Support/com.apple.sharedfilelist/')

def test_get_app_store_preferences_dir():
    assert config.get_app_store_preferences_dir() == path.join(
        config.get_home_dir(), 'Library/Containers/')
