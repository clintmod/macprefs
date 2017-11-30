from os import path
import logging as log
from utils import copy_dir, ensure_files_owned_by_user
from config import get_sys_preferences_backup_dir


def backup():
    log.info('Backing up system preferences... ')
    source = get_pm_path()
    dest = get_pm_backup_path()
    copy_dir(source, dest)


def restore():
    source = get_pm_backup_path()
    dest = get_pm_path()
    log.info('Restoring system preferences...')
    copy_dir(source, dest, with_sudo=True)
    ensure_files_owned_by_user('root:wheel', [dest], '644')


pm_file_name = 'com.apple.PowerManagement.plist'

def get_pm_backup_path():
    return path.join(get_sys_preferences_backup_dir(), pm_file_name)


def get_pm_path():
    pm_path = path.join('/Library/Preferences/', pm_file_name)
    if not path.exists(pm_path):
        pm_path = path.join('/Library/Preferences/SystemConfiguration/', pm_file_name)
    return pm_path
