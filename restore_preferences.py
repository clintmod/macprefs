import os
from config import BACKUP_DIR
from utils import executeShell

def restore():
  for filename in sorted(os.listdir(BACKUP_DIR)):
    if not ".plist" in filename: continue
    domain = filename.replace(".plist","")
    print "Importing: " + domain
    executeShell(["defaults", "import", domain, os.path.join(BACKUP_DIR, filename)])

if __name__ == '__main__':
  restore()