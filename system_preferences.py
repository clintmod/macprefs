from os import path
from utils import execute_shell
from config import get_sys_preferences_backup_dir


def backup():
    print ''
    print 'Backing up system preferences...'
    power_management_domain = get_domain()
    power_management_path = get_pm_backup_path()
    # On older versions of Mac OS X PowerManagement lived under SystemConfiguration
    print "Backing up: " + power_management_domain + " to " + power_management_path
    # sudo is not required to back up but it is to restore
    execute_shell(["defaults", "export", power_management_domain,
                   power_management_path])


def restore():
    print ''
    print 'Restoring system preferences...'
    power_management_domain = get_domain()
    power_management_restore_path = get_pm_backup_path()
    print "Restoring: " + power_management_domain + " from " + \
        power_management_restore_path
    result = execute_shell(
        ["sudo", "bash", "-c", "defaults import " +
         power_management_domain + " " + power_management_restore_path]
    )
    if result is not None:
        print result


def get_pm_backup_path():
    return path.join(get_sys_preferences_backup_dir(), "com.apple.PowerManagement.plist")


def get_domain():
    power_management_domain = "/Library/Preferences" + \
        "/com.apple.PowerManagement.plist"
    if not path.exists(power_management_domain):
        power_management_domain = "/Library/Preferences/" + \
            "SystemConfiguration/com.apple.PowerManagement.plist"
    return power_management_domain.replace('.plist', '')
