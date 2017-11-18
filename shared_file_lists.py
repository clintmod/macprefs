from os import path
from utils import execute_shell
import config


def backup():
    source = path.expanduser('~/Library/Application Support/com.apple.sharedfilelist')
    dest = path.join(config.get_backup_dir(), 'SharedFileLists')
    result = execute_shell(['cp', '-r', source, dest])
    if result is not None:
        print result

def restore():
    dest = path.expanduser('~/Library/Application Support/com.apple.sharedfilelist')
    source = path.join(config.get_backup_dir(), 'SharedFileLists')
    result = execute_shell(['cp', '-r', source, dest])
    if result is not None:
        print result