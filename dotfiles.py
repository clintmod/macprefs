from os import path, listdir
from config import get_dotfiles_backup_dir, get_dotfile_excludes, get_home_dir
from utils import execute_shell

def backup():
    #build file list
    home_dir = get_home_dir()
    files = []
    excludes = get_dotfile_excludes()
    for f in listdir(home_dir):
        full_file_path = path.join(home_dir, f)
        if path.isfile(full_file_path) and f[0] == '.' and f not in excludes:
            files.append(full_file_path)
    files.sort()
    dest = get_dotfiles_backup_dir()
    command = ['cp', '-a', '-v'] + files + [dest]
    print 'Backuping up dotfiles (e.g. ~/.bash_profile)...'
    output = execute_shell(command)
    if output is not None:
        print output

def restore():
    source = get_dotfiles_backup_dir()
    dest = get_home_dir()
    files = []
    for f in listdir(source):
        files.append(path.join(source, f))
    command = ['cp', '-a', '-v'] + files + [dest]
    print 'Restoring dotfiles to $HOME...'
    output = execute_shell(command)
    if output is not None:
        print output