from os import path
from utils import execute_shell
import config


def backup():
    print 'Backing up shared file lists...'
    source = path.expanduser(
        '~/Library/Application Support/com.apple.sharedfilelist/')
    dest = config.get_shared_file_lists_backup_dir() + "/"
    command = ['cp', '-r', source, dest]
    result = execute_shell(command)
    if result is not None:
        print result


def restore():
    print 'Restoring up shared file lists...'
    dest = path.expanduser(
        '~/Library/Application Support/com.apple.sharedfilelist/')
    source = config.get_shared_file_lists_backup_dir() + "/"
    command = ['cp', '-r', source, dest]
    result = execute_shell(command)
    if result is not None:
        print result
