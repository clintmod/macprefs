import os
from os import path
import sys
from utils import execute_shell
from config import get_sys_preferences_backup_dir


def backup():
    print ''
    print 'Backing up system preferences...'
    power_management_domain = get_domain()
    power_management_path = path.join(get_sys_preferences_backup_dir(), "com.apple.PowerManagement.plist")
    # On older versions of Mac OS X PowerManagement lived under SystemConfiguration
    print "Backing up: " + power_management_domain + " to " + power_management_path
    # sudo is not required to back up but it is to restore
    execute_shell(["defaults", "export", power_management_domain,
                   power_management_path])


def get_domain():
    pm = get_pm_file_path()
    return pm.replace('.plist', '')


def get_pm_file_path():
    power_management_domain = "/Library/Preferences" + \
        "/com.apple.PowerManagement.plist"
    if not path.exists(power_management_domain):
        power_management_domain = "/Library/Preferences/" + \
            "SystemConfiguration/com.apple.PowerManagement.plist"
    return power_management_domain


def restore():
    print ''
    print 'Restoring system preferences...'
    power_management_domain = get_domain()
    power_management_restore_path = get_pm_file_path()
    if os.getuid() != 0:
        print "Error: sudo is required to restore preferences: (e.g. sudo " + \
            sys.argv[0] + " restore)"
        sys.exit(1)
    print "Restoring: " + power_management_domain + " from " + \
        power_management_restore_path
    execute_shell(["defaults", "import", power_management_domain,
                   power_management_restore_path])
