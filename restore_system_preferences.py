import os
import sys
from config import get_backup_dir
from utils import execute_shell

power_management_restore_path = os.path.join(
    get_backup_dir(), "System", "com.apple.PowerManagement.plist")

power_management_domain = "/Library/Preferences/com.apple.PowerManagement"


def restore():
    if os.getuid() != 0:
        print "Error: sudo is required to restore preferences: (e.g. sudo " + sys.argv[0] + " restore)"
        sys.exit(1)
    print "Restoring: " + power_management_domain + " from " + power_management_restore_path
    execute_shell(["defaults", "import", power_management_domain,
                   power_management_restore_path])


if __name__ == '__main__':
    restore()
