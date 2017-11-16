import os
from os import path
import config


def test_get_backup_dir():
    backup_dir = config.get_backup_dir()
    assert backup_dir is not None

def test_get_backup_dir_works_with_environ():
    os.environ['MACPREFS_BACKUP_DIR'] = "asdf"
    backup_dir = config.get_backup_dir()
    assert "asdf" in backup_dir


def test_get_backup_file_path():
    assert config.get_backup_file_path("asdf.com") == path.join(
        config.get_backup_dir(), "asdf.com.plist")
