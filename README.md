# Mac Preferences Backup

A couple of python scripts to backup and restore Mac preferences using `defaults export` and `defaults import`.

This will backup Application as well as System Preferences.

## Requirements

- Mac OS X greater than 10.9 (maybe older… didn't test)
- Python 2.7 (Installed by default on Mac OS X > 10.9)

## Getting started

- clone or download this repo
- Open Terminal.app
- `cd` to the dir with this code in it

## Config

You can change `BACKUP_DIR` in config.py to a directory where you want to backup your Mac preferences too. The default is `~/Dropbox/MacPrefsBackup`

By default the script does not create the folder you want to back up too. It must already exist.

## Backing up

After you've configured `BACKUP_DIR`, you can run `python backup_preferences.py`.

## Restoring

You can restore your preferences by running `python restore_preferencs.py`.

## What it does

All the preferences for the domains listed by running `defaults domains` + `NSGlobalDomain` (NSGlobalDomain is System Preferences)

## Notes

- These scripts depend on `defaults domains` and is not compatible with the way [Mackup](https://github.com/lra/mackup) uses symlinks. On the bright side though, if you use this as well as Mackup to backup and restore, everything should just work. Just remember that anything Mackup backs up won't be backed up by these scripts.
