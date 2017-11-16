from os import path
from utils import execute_shell
from config import get_backup_dir


def backup():
    power_management_domain = get_domain()
    power_management_backup_path = path.join(
        get_backup_dir(), "System", "com.apple.PowerManagement.plist")
    # On older versions of Mac OS X PowerManagement lived under SystemConfiguration
    print "Backing up: " + power_management_domain + " to " + power_management_backup_path
    # sudo is not required to back up but it is to restore
    execute_shell(["defaults", "export", power_management_domain,
                   power_management_backup_path], False)


def get_domain():
    power_management_domain = "/Library/Preferences/com.apple.PowerManagement"
    if not path.exists(power_management_domain + ".plist"):
        power_management_domain = "/Library/Preferences/SystemConfiguration/com.apple.PowerManagement"
    return power_management_domain


if __name__ == '__main__':
    backup()
