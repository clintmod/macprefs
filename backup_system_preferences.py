import os
import sys
from utils import executeShell
from config import BACKUP_DIR

def backup():
  power_management_backup_path = os.path.join(BACKUP_DIR, "System", "com.apple.PowerManagement.plist")
  power_management_domain = "/Library/Preferences/com.apple.PowerManagement"
  # On older versions of Mac OS X PowerManagement lived under SystemConfiguration
  if not os.path.exists(power_management_domain+".plist"):
      power_management_domain = "/Library/Preferences/SystemConfiguration/com.apple.PowerManagement"
  print "Backing up: " + power_management_domain + " to " + power_management_backup_path
  # sudo is not required to back up but it is to restore
  executeShell(["defaults", "export", power_management_domain, power_management_backup_path], False)

if __name__ == '__main__':
  backup()