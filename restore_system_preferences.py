import os
import sys
from config import BACKUP_DIR
from utils import executeShell

def restore():
  power_management_restore_path = os.path.join(BACKUP_DIR, "System", "com.apple.PowerManagement.plist")
  power_management_domain = "/Library/Preferences/com.apple.PowerManagement"
  print "Restoring: " + power_management_domain + " from " + power_management_restore_path
  executeShell(["defaults", "import", power_management_domain, power_management_restore_path], False)

if __name__ == '__main__':
  if os.getuid() != 0:
    print "sudo is required to restore these preferences: (e.g. sudo python restore_system_preferences.py)"
    sys.exit()
  restore()