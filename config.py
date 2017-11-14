import os
from os import path

BACKUP_DIR = os.environ['MACPREFS_BACKUP_DIR'] if 'MACPREFS_BACKUP_DIR' in os.environ else path.join(path.expanduser("~"), "Dropbox", "MacPrefsBackup")