from os import environ, makedirs, path


def get_macprefs_dir():
    backup_dir = ""
    if 'MACPREFS_BACKUP_DIR' in environ:
        backup_dir = environ['MACPREFS_BACKUP_DIR']
    else:
        backup_dir = path.join(get_home_dir(), "Dropbox", "MacPrefsBackup")
    ensure_exists(backup_dir)
    return backup_dir


def get_preferences_backup_dir():
    return_val = path.join(get_macprefs_dir(), "preferences/")
    ensure_exists(return_val)
    return return_val


def get_preferences_path(domain):
    return path.join(get_preferences_backup_dir(), domain + ".plist")


def get_sys_preferences_backup_dir():
    return_val = path.join(get_macprefs_dir(), "system_preferences/")
    ensure_exists(return_val)
    return return_val


def get_shared_file_lists_backup_dir():
    return_val = path.join(get_macprefs_dir(), "shared_file_lists/")
    ensure_exists(return_val)
    return return_val


def get_shared_file_lists_dir():
    return path.expanduser('~/Library/Application Support/com.apple.sharedfilelist/')


def get_dotfiles_backup_dir():
    return_val = path.join(get_macprefs_dir(), "dotfiles/")
    ensure_exists(return_val)
    return return_val


def get_dotfile_excludes():
    return ['.CFUserTextEncoding', '.DS_Store']


def get_home_dir():
    return path.expanduser('~') + '/'


def ensure_exists(input_dir):
    if not path.exists(input_dir):
        makedirs(input_dir)
