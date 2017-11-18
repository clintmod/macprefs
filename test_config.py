import os
from os import path
import config
from mock import patch

def test_get_backup_dir():
    backup_dir = config.get_backup_dir()
    assert backup_dir is not None

@patch("config.makedirs")
def test_get_backup_dir_works_with_environ(makedirs_mock):
    os.environ['MACPREFS_BACKUP_DIR'] = "asdf"
    backup_dir = config.get_backup_dir()
    del os.environ['MACPREFS_BACKUP_DIR']
    assert "asdf" in backup_dir

@patch("config.path.exists")
@patch("config.makedirs")
def test_get_backup_makes_the_dir_if_it_not_exists(exists_mock, makedirs_mock):
    exists_mock.return_value = False
    config.get_backup_dir()
    makedirs_mock.assert_called_once()


def test_get_file_path():
    assert config.get_file_path("asdf.com") == path.join(
        config.get_backup_dir(), "asdf.com.plist")
