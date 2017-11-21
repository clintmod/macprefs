from utils import copy_files
import config


def backup():
    print ''
    print 'Backing up shared file lists...'
    source = config.get_shared_file_lists_dir()
    dest = config.get_shared_file_lists_backup_dir()
    copy_files(source, dest)


def restore():
    print ''
    print 'Restoring up shared file lists...'
    dest = config.get_shared_file_lists_dir()
    source = config.get_shared_file_lists_backup_dir()
    copy_files(source, dest)
