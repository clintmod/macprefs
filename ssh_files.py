from config import get_ssh_backup_dir, get_ssh_user_dir, get_user
from utils import copy_files, ensure_owned_by_user


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
    copy_files(
        source, dest, as_archive=False,
        as_dir=True, with_sudo=True
    )
    ensure_owned_by_user(dest, get_user())
