import os
from os import path


def get_backup_dir():
    backup_dir = ""
    if 'MACPREFS_BACKUP_DIR' in os.environ:
        backup_dir = os.environ['MACPREFS_BACKUP_DIR']
    else:
        backup_dir = path.join(path.expanduser(
            "~"), "Dropbox", "MacPrefsBackup")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    return backup_dir


def get_backup_file_path(domain):
    return path.join(get_backup_dir(), domain + ".plist")
