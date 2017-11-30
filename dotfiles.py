from os import path, listdir
import logging as log
from config import get_dotfiles_backup_dir, get_dotfile_excludes, get_home_dir, get_user
from utils import copy_files, ensure_files_owned_by_user


def backup():
    log.info('Backing up dotfiles...')
    # build file list
    home_dir = get_home_dir()
    excludes = get_dotfile_excludes()
    files = get_dot_files(home_dir, excludes)
    dest = get_dotfiles_backup_dir()
    copy_files(files, dest)


def restore():
    log.info('Restoring dotfiles...')
    source = get_dotfiles_backup_dir()
    dest = get_home_dir()
    files = get_dot_files(source)
    copy_files(files, dest)
    files = get_dot_files(dest)
    ensure_files_owned_by_user(get_user(), files)


def get_dot_files(home_dir, excludes=None):
    if excludes is None:
        excludes = []
    files = []
    for f in listdir(home_dir):
        full_file_path = path.join(home_dir, f)
        if f[0] == '.' and path.isfile(full_file_path) and f not in excludes:
            files.append(full_file_path)
    return files
