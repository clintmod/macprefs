from config import get_preferences_backup_dir, get_preferences_dir, get_user

from utils import copy_files, ensure_dir_owned_by_user


def backup():
    print ''
    print 'Backing up preferences (.plist)...'
    print ''
    source = get_preferences_dir()
    dest = get_preferences_backup_dir()
    copy_files(source, dest)


def restore():
    print ''
    print 'Restoring preferences (.plist)...'
    print ''
    source = get_preferences_backup_dir()
    dest = get_preferences_dir()
    copy_files(source, dest, with_sudo=True)
    ensure_dir_owned_by_user(dest, get_user())
