from os import environ, makedirs, path, getenv
import getpass


def get_macprefs_dir():
    backup_dir = ''
    if 'MACPREFS_BACKUP_DIR' in environ:
        backup_dir = environ['MACPREFS_BACKUP_DIR']
    else:
        backup_dir = path.join(get_home_dir(), 'Dropbox', 'MacPrefsBackup')
    ensure_exists(backup_dir)
    return backup_dir


def get_preferences_dir():
    return_val = path.join(get_home_dir(), 'Library/Preferences/')
    return return_val


def get_preferences_backup_dir():
    return_val = path.join(get_macprefs_dir(), 'preferences/')
    ensure_exists(return_val)
    return return_val


def get_sys_preferences_backup_dir():
    return_val = path.join(get_macprefs_dir(), 'system_preferences/')
    ensure_exists(return_val)
    return return_val


def get_shared_file_lists_backup_dir():
    return_val = path.join(get_macprefs_dir(), 'shared_file_lists/')
    ensure_exists(return_val)
    return return_val


def get_shared_file_lists_dir():
    return path.join(get_home_dir(), 'Library/Application Support/com.apple.sharedfilelist/')


def get_dotfiles_backup_dir():
    return_val = path.join(get_macprefs_dir(), 'dotfiles/')
    ensure_exists(return_val)
    return return_val


def get_dotfile_excludes():
    return ['.CFUserTextEncoding', '.DS_Store']


def get_home_dir():
    return getenv('HOME') + '/'


def ensure_exists(input_dir):
    if not path.exists(input_dir):
        makedirs(input_dir)


def get_ssh_backup_dir():
    return_val = path.join(get_macprefs_dir(), 'ssh/')
    ensure_exists(return_val)
    return return_val


def get_ssh_user_dir():
    return_val = path.join(get_home_dir(), '.ssh/')
    return return_val


def get_user():
    return getpass.getuser()


def get_internet_accounts_dir():
    return path.join(get_home_dir(), 'Library/Accounts/')


def get_internet_accounts_backup_dir():
    return_val = path.join(
        get_macprefs_dir(), 'Accounts/')
    ensure_exists(return_val)
    return return_val


def get_user_launch_agents_dir():
    return path.join(get_home_dir(), 'Library/LaunchAgents/')


def get_user_launch_agents_backup_dir():
    return_val = path.join(
        get_macprefs_dir(), 'StartupItems/LaunchAgents/User/')
    ensure_exists(return_val)
    return return_val


def get_system_launch_agents_dir():
    return '/Library/LaunchAgents/'


def get_system_launch_agents_backup_dir():
    return_val = path.join(
        get_macprefs_dir(), 'StartupItems/LaunchAgents/AllUsers/')
    ensure_exists(return_val)
    return return_val


def get_system_launch_daemons_dir():
    return '/Library/LaunchDaemons/'


def get_system_launch_daemons_backup_dir():
    return_val = path.join(
        get_macprefs_dir(), 'StartupItems/LaunchDaemons/AllUsers/')
    ensure_exists(return_val)
    return return_val


def get_app_store_preferences_dir():
    return_val = path.join(get_home_dir(), 'Library/Containers/')
    return return_val


def get_app_store_preferences_backup_dir():
    return_val = path.join(get_macprefs_dir(), 'app_store_preferences/')
    ensure_exists(return_val)
    return return_val
