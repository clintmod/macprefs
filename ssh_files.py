from config import get_ssh_backup_dir, get_ssh_user_dir
from utils import copy_files


def backup():
    print ''
    print 'Backuping up .ssh dir...'
    source = get_ssh_user_dir()
    dest = get_ssh_backup_dir()
    copy_files(source, dest)


def restore():
    print ''
    print 'Restoring .ssh dir...'
    source = get_ssh_backup_dir()
    dest = get_ssh_user_dir()
    copy_files(source, dest)
