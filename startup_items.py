import logging as log
from utils import copy_dir, ensure_dir_owned_by_user
import config


def backup():
    log.info('Backing up start up items...')
    backup_user_launch_agents()
    backup_system_launch_agents()
    backup_system_daemons_agents()


def restore():
    log.info('Restoring start up items...')
    restore_user_launch_agents()
    restore_system_launch_agents()
    restore_system_daemons_agents()


def backup_user_launch_agents():
    source = config.get_user_launch_agents_dir()
    dest = config.get_user_launch_agents_backup_dir()
    copy_dir(source, dest)


def backup_system_launch_agents():
    source = config.get_system_launch_agents_dir()
    dest = config.get_system_launch_agents_backup_dir()
    copy_dir(source, dest)


def backup_system_daemons_agents():
    source = config.get_system_launch_daemons_dir()
    dest = config.get_system_launch_daemons_backup_dir()
    copy_dir(source, dest)


def restore_user_launch_agents():
    source = config.get_user_launch_agents_backup_dir()
    dest = config.get_user_launch_agents_dir()
    copy_dir(source, dest, with_sudo=True)
    ensure_dir_owned_by_user(dest, config.get_user())


def restore_system_launch_agents():
    source = config.get_system_launch_agents_backup_dir()
    dest = config.get_system_launch_agents_dir()
    copy_dir(source, dest, with_sudo=True)
    ensure_dir_owned_by_user(dest, 'root:wheel', '644')


def restore_system_daemons_agents():
    source = config.get_system_launch_daemons_backup_dir()
    dest = config.get_system_launch_daemons_dir()
    copy_dir(source, dest, with_sudo=True)
    ensure_dir_owned_by_user(dest, 'root:wheel', '644')
