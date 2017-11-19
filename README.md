# Mac Preferences Backup

A tool to backup and restore Mac preferences.

This will backup and restore Application as well as System Preferences.

## Motivation (.macos problems)

I wanted a solution to back up my settings for my Mac and one didn't really exist. Time Machine is a bit overkill for this.

At first I was trying to create a bash script to restore all my settings. I was trying to adapt the ~~`.osx`~~ `.macos` file from [Mathias Bynens](https://github.com/mathiasbynens/dotfiles/blob/master/.macos). I noticed that some of the cases for the domains were wrong/outdated and weren't actually changing the preferences they were intended to change.

Running `defaults write` with the wrong case also caused problems while trying create this tool because of [Case Conflicts](#case-conflicts).

## Requirements

- Mac OS X greater than 10.9 (maybe older… didn't test)
- Python 2.7 (Installed by default on Mac OS X > 10.6)

## Installation

Install [Homebrew](https://brew.sh/)

``` bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Tap into my [homebrew formulas](https://github.com/clintmod/homebrew-formulas):

``` bash
brew tap clintmod/formulas
```

Install via homebrew

``` bash
brew install macprefs
```

## Config

You can set the MACPREFS_BACKUP_DIR environment variable to specify where you'd like to backup the prefs too.

The default backup directory is `~/Dropbox/MacPrefsBackup`.

```bash
export MACPREFS_BACKUP_DIR="$HOME/SomeOtherDir"
```

## Backing Up

You can backup your preferences by running:

``` bash
macprefs backup
```

## Restoring

You can restore your preferences by running (restoring requires sudo to restore PowerManagment settings):

``` bash
sudo macprefs restore
```

- **You might have to log out and then log back in for the settings to take effect.**

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

- Backs up all the preferences for the domains listed by running `defaults domains` + `NSGlobalDomain` (NSGlobalDomain contains some system preferences)
- Backs up PowerManagement preferences

## Notes

- ### Mackup
  - These scripts depend on `defaults domains` and is not compatible with the way [Mackup](https://github.com/lra/mackup) uses symlinks. On the bright side though, if you use this as well as Mackup to backup and restore, everything should just work. Just remember that any preferences Mackup backs up won't be backed up by this tool.

- ### Case Conflicts
  - It's possible that software companies (Apple included) change the case of the bundle id for an Application. This can cause multiple plist files to appear in `~/Library/Preferences/`. This causes a problem with the this tool. As `defaults domains` will report the domains with a (Case Conflict). To resolve this you can open the problem file located in ~/Library/Preferences/ with XCode to determine which is the correct one with the correct case and delete the other one. The incorrect one will most likely have one or two values in it as compared to many values in the other.

- ### Using `defaults write`
  - When you run `defaults write` and use the wrong/old case for the domain you can also get [Case Conflicts](#case-conflicts). (e.g. com.apple.addressbook instead of com.apple.AddressBook).
  - The `defaults` app has a tendency to fail silently for some things. You might be trying to use old `defaults write` commands where key is the wrong name.
  - Because of the above 2 reasons maintaining a bunch of `defaults write` commands in bash script can be difficult

## Todo

- [x] Backup and restore `/Library/Preferences` (e.g. PowerManagement)
- [x] Installable via homebrew
- [x] Backup and restore shared file lists (Finder sidebar) `~/Library/Application Support/com.apple.sharedfilelist`
- [x] Backup and restore dotfiles (e.g. $HOME/.bash_profile)
- [ ] Write a util to generate a `bash` script of `defaults write` commands by diffing a new user account against the owned account

## Problems

- If you find a problem or a have a question feel free to file a bug here and/or send a pull request and I'll be happy to look at it and/or merge it.

## Contributing

### Getting started

- Fork and clone then cd to this git repo
- Run `pip install -r requirements.txt`

### Running the tests

- Run `make test lint` (make sure you've done the [Getting Started](#getting-started))

### Getting your changes merged

- Make your changes and push them to github
- Make sure your changes have tests and pass linting
- Open a pull request
