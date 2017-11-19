from utils import execute_shell
import config


def backup():
    print 'Backing up shared file lists...'
    source = config.get_shared_file_lists_dir()
    dest = config.get_shared_file_lists_backup_dir()
    command = ['cp', '-a', '-v', source, dest]
    result = execute_shell(command)
    if result is not None:
        print result


def restore():
    print 'Restoring up shared file lists...'
    dest = config.get_shared_file_lists_dir()
    source = config.get_shared_file_lists_backup_dir()
    command = ['cp', '-a', '-v', source, dest]
    result = execute_shell(command)
    if result is not None:
        print result
