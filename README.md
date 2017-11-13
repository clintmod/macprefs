# Mac Preferences Backup

A couple of python scripts to backup and restore Mac preferences using `defaults export` and `defaults import`.

This will backup and restore Application as well as System Preferences.

## Requirements

- Mac OS X greater than 10.9 (maybe older… didn't test)
- Python 2.7 (Installed by default on Mac OS X > 10.9)

## Getting started

- Clone or download this repository
- Open Terminal.app
- `cd` to the dir with this code in it

## Config

You can change `BACKUP_DIR` in config.py to a directory where you want to backup your Mac preferences too. The default is `~/Dropbox/MacPrefsBackup`

## Backing up

After you've configured `BACKUP_DIR`, you can run `python backup_preferences.py`.

## Restoring

You can restore your preferences by running `python restore_preferences.py`.

You might have to log out and then log back in for the setting to take effect.

## Testing the Restore (You should)

- Create a new user on your Mac
- Log in as that user
- Do the [Getting Started](#getting-started)
- Update the [Config](#config)
- Run the [Restore](#restoring)

## What it does

It backs up all the preferences for the domains listed by running `defaults domains` + `NSGlobalDomain` (NSGlobalDomain contains some system properties)

## Notes

- These scripts depend on `defaults domains` and is not compatible with the way [Mackup](https://github.com/lra/mackup) uses symlinks. On the bright side though, if you use this as well as Mackup to backup and restore, everything should just work. Just remember that anything Mackup backs up won't be backed up by these scripts.
- Case Conflicts - It's possible that software companies (Apple included) change the case of the bundle id for an Application. This can also happen when you run `defaults write` and use the wrong (or old) case for the domain. (e.g. com.apple.addressbook instead of com.apple.AddressBook) .This can cause multiple plist files to appear in `~/Library/Preferences/`. To resolve this you can open the file with XCode to determine which is the correct one with the correct case and delete the other one.
