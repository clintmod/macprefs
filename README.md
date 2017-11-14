# Mac Preferences Backup

Some python scripts to backup and restore Mac preferences using `defaults export` and `defaults import`.

This will backup and restore Application as well as System Preferences.

## Motiviation (.macos problems)

I was trying to adapt the ~~`.osx`~~ `.macos` file from [Mathias Bynens](https://github.com/mathiasbynens/dotfiles/blob/master/.macos) and noticed that some of the cases for the domains were wrong and weren't actually changing the preferences they were intended to change. This also caused problems while trying to diff the changes as I was seeing because of [Case Conflicts](#case-conflicts).

So I decided to write some scripts that use the standard api for importing and exporting `defaults`.

## Requirements

- Mac OS X greater than 10.9 (maybe older… didn't test)
- Python 2.7 (Installed by default on Mac OS X > 10.9)

## Getting Started

- Clone or download this repository
- Open Terminal.app
- `cd` to the dir with this code in it

## Config

You can change `BACKUP_DIR` in config.py to a directory where you want to backup your Mac preferences too. The default is `~/Dropbox/MacPrefsBackup`

## Backing Up

After you've configured `BACKUP_DIR`, you can run:

``` bash
python backup_preferences.py
```

## Restoring

You can restore your preferences by running 

``` bash
python restore_preferences.py
```

- **You might have to log out and then log back in for the setting to take effect.**

## Testing the Restore

- Create a new user on your Mac
- Log in as that user
- Do the [Getting Started](#getting-started)
- Update the [Config](#config)
- You might have to grant the new user access to your backup files
  - `sudo chmod 660 -R [BACKUP_DIR] && sudo chmod -R ug+X ~/Dropbox/MacPrefsBackup`
- Run the [Restore](#restoring)
- Log out and log back in

## What it Does

It backs up all the preferences for the domains listed by running `defaults domains` + `NSGlobalDomain` (NSGlobalDomain contains some system preferences)

## Notes

- ### Mackup
  - These scripts depend on `defaults domains` and is not compatible with the way [Mackup](https://github.com/lra/mackup) uses symlinks. On the bright side though, if you use this as well as Mackup to backup and restore, everything should just work. Just remember that any preferences Mackup backs up won't be backed up by these scripts.

- ### Case Conflicts
  - It's possible that software companies (Apple included) change the case of the bundle id for an Application. This can cause multiple plist files to appear in `~/Library/Preferences/`. This can cause a problem with the scripts. As `defaults domains` will report the domains with a (Case Conflict). To resolve this you can open the problem file located in ~/Library/Preferences/ with XCode to determine which is the correct one with the correct case and delete the other one.

- ### Using `defaults write`
  - When you run `defaults write` and use the wrong (or old) case for the domain you can also get [Case Conflicts](#case-conflicts). (e.g. com.apple.addressbook instead of com.apple.AddressBook).
  - The `defaults` app has a tendency to fail silently for some things. You might be trying to use old `defaults write` commands where key is the wrong name.
  - Because of the above 2 reasons maintaining a bunch of `defaults write` commands in bash script can be difficult

## Todo

- Backup and restore `/Library/Preferences` (e.g. PowerManagement)
- Backup and restore shared lists `~Library/Application Support/com.apple.sharedfilelist`
- Write a util to generate a bash script of `defaults write` commands that diffs a new user account against your own account

## Problems

- If you find a problem or a have a question feel free to file a bug here and/or send a pull request and I'll be happy to look at it and/or merge it.