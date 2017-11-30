import logging as log
from config import get_preferences_backup_dir, get_preferences_dir, get_user
from utils import copy_dir, ensure_dir_owned_by_user


def backup():
    log.info('Backing up preferences (.plist)...')
    source = get_preferences_dir()
    dest = get_preferences_backup_dir()
    copy_dir(source, dest)


def restore():
    log.info('Restoring preferences (.plist)...')
    source = get_preferences_backup_dir()
    dest = get_preferences_dir()
    copy_dir(source, dest, with_sudo=True)
    ensure_dir_owned_by_user(dest, get_user())
