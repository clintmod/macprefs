from os import path, listdir
from config import get_dotfiles_backup_dir, get_dotfile_excludes, get_home_dir
from utils import execute_shell

def backup():
    print ''
    print 'Backuping up dotfiles...'
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
    output = execute_shell(command)
    if output is not None:
        print output

def restore():
    print ''
    print 'Restoring dotfiles...'
    source = get_dotfiles_backup_dir()
    dest = get_home_dir()
    files = []
    for f in listdir(source):
        files.append(path.join(source, f))
    command = ['cp', '-a', '-v'] + files + [dest]
    output = execute_shell(command)
    if output is not None:
        print output