from os.path import exists
import logging as log
from utils import copy_dir, ensure_dir_owned_by_user
import config


def backup():
    log.info('Backing up shared file lists...')
    source = config.get_shared_file_lists_dir()
    if not exists(source):
        log.info('Warning: %s does not exist.', source)
        log.info('Shared file backup failed.')
        return
    dest = config.get_shared_file_lists_backup_dir()
    copy_dir(source, dest)


def restore():
    log.info('Restoring shared file lists...')
    dest = config.get_shared_file_lists_dir()
    source = config.get_shared_file_lists_backup_dir()
    copy_dir(source, dest, with_sudo=True)
    ensure_dir_owned_by_user(dest, config.get_user())
