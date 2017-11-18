from os import path, makedirs, environ

def get_backup_dir():
    backup_dir = ""
    if 'MACPREFS_BACKUP_DIR' in environ:
        backup_dir = environ['MACPREFS_BACKUP_DIR']
    else:
        backup_dir = path.join(path.expanduser(
            "~"), "Dropbox", "MacPrefsBackup")
    if not path.exists(backup_dir):
        makedirs(backup_dir)
    return backup_dir


def get_file_path(domain):
    return path.join(get_backup_dir(), domain + ".plist")
