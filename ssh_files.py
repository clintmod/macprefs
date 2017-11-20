from config import get_ssh_backup_dir, get_ssh_user_dir
from utils import execute_shell


def backup():
    print ''
    print 'Backuping up .ssh dir...'
    source = get_ssh_user_dir()
    dest = get_ssh_backup_dir()
    command = ['cp', '-a', '-v', source, dest]
    result = execute_shell(command)
    if result is not None:
        print result


def restore():
    print ''
    print 'Restoring .ssh dir...'
    source = get_ssh_backup_dir()
    dest = get_ssh_user_dir()
    command = ['cp', '-a', '-v', source, dest]
    result = execute_shell(command)
    if result is not None:
        print result
