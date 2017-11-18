from os import path, makedirs, environ


def get_macprefs_dir():
    backup_dir = ""
    if 'MACPREFS_BACKUP_DIR' in environ:
        backup_dir = environ['MACPREFS_BACKUP_DIR']
    else:
        backup_dir = path.join(path.expanduser(
            "~"), "Dropbox", "MacPrefsBackup")
    if not path.exists(backup_dir):
        makedirs(backup_dir)
    return backup_dir


def get_preferences_backup_dir():
    return path.join(get_macprefs_dir(), "preferences")


def get_preferences_path(domain):
    return path.join(get_preferences_backup_dir(), domain + ".plist")


def get_sys_preferences_backup_dir():
    return path.join(get_macprefs_dir(), "system_preferences")


def get_shared_file_lists_backup_dir():
    return path.join(get_macprefs_dir(), "shared_file_lists")


def get_dotfiles_backup_dir():
    return path.join(get_macprefs_dir(), "dotfiles")
