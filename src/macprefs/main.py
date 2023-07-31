import argparse
import sys
import logging as log
from macprefs import config
from macprefs.modules import (
    dotfiles,
    preferences,
    shared_file_lists,
    system_preferences,
    ssh_files,
    startup_items,
    app_store_preferences,
    internet_accounts,
)
from macprefs import __version__

preference_choices = [
    "system_preferences",
    "startup_items",
    "dotfiles",
    "shared_file_lists",
    "ssh_files",
    "preferences",
    "app_store_preferences",
    "internet_accounts",
]


def backup(choices=None):
    choices = choices or []
    if not choices or "system_preferences" in choices:
        system_preferences.backup()
    if not choices or "startup_items" in choices:
        startup_items.backup()
    if not choices or "dotfiles" in choices:
        dotfiles.backup()
    if not choices or "shared_file_lists" in choices:
        shared_file_lists.backup()
    if not choices or "ssh_files" in choices:
        ssh_files.backup()
    if not choices or "preferences" in choices:
        preferences.backup()
    if not choices or "app_store_preferences" in choices:
        app_store_preferences.backup()
    if not choices or "internet_accounts" in choices:
        internet_accounts.backup()
    print("Backup Complete.")


def restore(choices=None):
    choices = choices or []
    if not choices or "system_preferences" in choices:
        system_preferences.restore()
    if not choices or "startup_items" in choices:
        startup_items.restore()
    if not choices or "dotfiles" in choices:
        dotfiles.restore()
    if not choices or "shared_file_lists" in choices:
        shared_file_lists.restore()
    if not choices or "ssh_files" in choices:
        ssh_files.restore()
    if not choices or "preferences" in choices:
        preferences.restore()
    if not choices or "app_store_preferences" in choices:
        app_store_preferences.restore()
    if not choices or "internet_accounts" in choices:
        internet_accounts.restore()
    print("Restore Complete.")


def invoke_func(args):
    if args.func is not None:
        if args.name in ["backup", "restore"]:
            args.func(args.t)
        else:
            args.func()


def configure_logging(verbose):
    if verbose > 0:
        log.basicConfig(format="%(message)s", level=log.DEBUG)
        log.debug("Verbose logging enabled")
    else:
        log.basicConfig(format="%(message)s", level=log.INFO)


def main():
    backup_dir = config.get_macprefs_dir()
    parser = argparse.ArgumentParser(
        prog="macprefs",
        description="backup and restore mac system preferences",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--verbose", "-v", action="count", help="log everything to the console"
    )

    subparsers = parser.add_subparsers(title="commands", metavar="")

    backup_parser = subparsers.add_parser(
        "backup", help="backup preferences to " + backup_dir
    )
    backup_parser.set_defaults(name="backup", func=backup)
    backup_parser.add_argument(
        "-t",
        nargs="*",
        metavar="type",
        help="preferences you want to backup",
        choices=preference_choices,
        action="extend",
    )

    restore_parser = subparsers.add_parser(
        "restore", help="restore preferences from " + backup_dir
    )
    restore_parser.set_defaults(name="restore", func=restore)
    restore_parser.add_argument(
        "-t",
        nargs="*",
        metavar="type",
        help="preferences you want to restore",
        choices=preference_choices,
        action="extend",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args()
    verbosity = 0 if args.verbose is None else args.verbose
    configure_logging(verbosity)
    invoke_func(args)


if __name__ == "__main__":
    main()
