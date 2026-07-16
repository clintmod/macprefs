import logging as log
from utils import copy_dir, ensure_dir_owned_by_user
import config


def backup():
    log.info('Backing up internet accounts db files...')
    backup_internet_accounts()


def restore():
    log.info('Restoring internet accounts db files...')
    restore_internet_accounts()


def backup_internet_accounts():
    source = config.get_internet_accounts_dir()
    dest = config.get_internet_accounts_backup_dir()
    copy_dir(source, dest)


def restore_internet_accounts():
    source = config.get_internet_accounts_backup_dir()
    dest = config.get_internet_accounts_dir()
    copy_dir(source, dest, with_sudo=True)
    ensure_dir_owned_by_user(dest, config.get_user())
