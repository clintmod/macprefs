from os.path import exists
from config import get_ssh_backup_dir, get_ssh_user_dir, get_user, ensure_exists
from utils import copy_files, ensure_owned_by_user


def backup():
    print ''
    source = get_ssh_user_dir()
    if not exists(source):
        print 'No .ssh dir found... skipping.'
        return
    print 'Backuping up .ssh dir...'
    dest = get_ssh_backup_dir()
    ensure_exists(dest)
    copy_files(source, dest)


def restore():
    print ''
    source = get_ssh_backup_dir()
    if not exists(source):
        print 'No .ssh dir found... skipping.'
        return
    print 'Restoring .ssh dir...'
    dest = get_ssh_user_dir()
    copy_files(
        source, dest, as_archive=False,
        as_dir=True, with_sudo=True
    )
    ensure_owned_by_user(dest, get_user())