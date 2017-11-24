from utils import copy_dir, ensure_dir_owned_by_user
import config


def backup():
    print ''
    print 'Backing up shared file lists...'
    print ''
    source = config.get_shared_file_lists_dir()
    dest = config.get_shared_file_lists_backup_dir()
    copy_dir(source, dest)


def restore():
    print ''
    print 'Restoring shared file lists...'
    print ''
    dest = config.get_shared_file_lists_dir()
    source = config.get_shared_file_lists_backup_dir()
    copy_dir(source, dest, with_sudo=True)
    ensure_dir_owned_by_user(dest, config.get_user())
