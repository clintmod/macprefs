# Mac Preferences Backup

A tool to backup and restore Mac preferences.

This will backup and restore Application as well as System Preferences.

## Motivation (.macos problems)

I wanted a solution to back up my settings for my Mac and one didn't really exist. Time Machine is a bit overkill for this.

At first I was trying to create a bash script to restore all my settings. I was trying to adapt the ~~`.osx`~~ `.macos` file from [Mathias Bynens](https://github.com/mathiasbynens/dotfiles/blob/master/.macos). I noticed that some of the cases for the domains were wrong/outdated and weren't actually changing the preferences they were intended to change.

Running `defaults write` with the wrong case for the keys or domains also causes problems as the defaults command may fail silently.

## Requirements

- Mac OS X greater than 10.9 (maybe older… didn't test)
- Python 3.6

## Installation

Install [Homebrew](https://brew.sh/)

``` bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

``` bash
brew install clintmod/formulas/macprefs
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

You can restore your preferences by running:

``` bash
macprefs restore
```

- **You might have to log out and then log back in for the settings to take effect.**

## Testing the Restore

- Create a new user on your Mac
- Make sure he's in the admin group
- Log in as that user
- Do the [Getting Started](#getting-started) steps
- Update the [Config](#config)
- Grant the admin group read access to your backup files (substitute ~/Dropbox with your backup dir if different)

```bash
# grant admin group read on ~/Dropbox
chmod +a "group:admin allow list,search,readattr,readextattr,readsecurity" ~/Dropbox/
# grant admin group read on ~/Dropbox/MacPrefsBackup recursively (-R)
chmod -R +a "group:admin allow list,search,readattr,readextattr,readsecurity" ~/Dropbox/MacPrefsBackup
# grant dir list (execute) permission on all subfolders of ~/Dropbox recursively (-R)
chmod -R +X ~/Dropbox
# remove execute permission for other on all files and folders because
# +X adds other permissions
chmod -R o=-x ~/Dropbox
```

- Run the [Restore](#restoring)
- Log out and log back in to confirm the restore succeeded

## What it Does

- Backs up all the preferences in `~/Library/Preferences` and `/Library/Preferences`
- Backs up all 'Internet Accounts' databases in `~/Library/Accounts`
- Backs up PowerManagement preferences
- Backs up shared file lists (Finder Favorites in Sidebar) `~/Library/Application Support/com.apple.sharedfilelist`
- Backups up dotfiles ($HOME/.* (e.g. .bash_profile))
- Backups up the $HOME/.ssh dir
- Backups launch items `/Library/LaunchAgents`, `/Library/LaunchDaemons`, `~/Library/LaunchAgents`

## Notes

- ### Mackup
  - These scripts makes copies of plist files in `~/Library/Preferences` and is not compatible with the way [Mackup](https://github.com/lra/mackup) creates symlinks for some of these files. On the bright side though, if you use this as well as Mackup to backup and restore, everything should just work. Just remember that any preferences Mackup backs up won't be backed up by this tool.

- ### Using `defaults write`
  - When you run `defaults write` and use the wrong/old case for the domain you can create a new plist file with the wrong case (e.g. com.apple.addressbook instead of com.apple.AddressBook).
  - The `defaults` app has a tendency to fail silently for some things. You might be trying to use old `defaults write` commands where the key is the wrong name.
  - Because of the above 2 reasons maintaining a bunch of `defaults write` commands in bash script can be error prone and the defaults command will fail silently.

## Todo

- [x] Backup and restore `/Library/Preferences` (e.g. PowerManagement)
- [x] Installable via homebrew
- [x] Backup and restore shared file lists (Finder sidebar) `~/Library/Application Support/com.apple.sharedfilelist`
- [x] Backup and restore dotfiles (e.g. $HOME/.bash_profile)
- [x] $HOME/.ssh dir
- [x] Startup Items `/Library/LaunchAgents`, `/Library/LaunchDaemons`, `~/Library/LaunchAgents`
- [ ] Verify backup and restore
- [ ] Write a util to generate a `bash` script of `defaults write` commands by diffing a new user account against the owned account

## Problems

- If you find a problem or a have a question feel free to file a bug here and/or send a pull request and I'll be happy to look at it and/or merge it.

## Contributing

### Getting started

- Fork and clone then cd to this git repository
- Run `pip install -r requirements.txt`

### Running the tests

- Run `make test lint` (make sure you've done the [Getting Started](#getting-started))

### Getting your changes merged

- Make your changes and push them to github
- Make sure your changes have tests and pass linting
- Open a pull request
