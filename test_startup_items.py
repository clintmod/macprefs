from mock import patch

import startup_items
import config

@patch('startup_items.backup_system_daemons_agents')
@patch('startup_items.backup_system_launch_agents')
@patch('startup_items.backup_user_launch_agents')
def test_backup(user_agents_mock, system_agents_mock, system_daemons_mock):
    startup_items.backup()
    user_agents_mock.assert_called_once()
    system_agents_mock.assert_called_once()
    system_daemons_mock.assert_called_once()


@patch('startup_items.restore_system_daemons_agents')
@patch('startup_items.restore_system_launch_agents')
@patch('startup_items.restore_user_launch_agents')
def test_restore(user_agents_mock, system_agents_mock, system_daemons_mock):
    startup_items.restore()
    user_agents_mock.assert_called_once()
    system_agents_mock.assert_called_once()
    system_daemons_mock.assert_called_once()


@patch('startup_items.copy_dir')
def test_backup_user_launch_agents(copy_mock):
    source = config.get_user_launch_agents_dir()
    dest = config.get_user_launch_agents_backup_dir()
    startup_items.backup_user_launch_agents()
    copy_mock.assert_called_with(
        source, dest
    )


@patch('startup_items.copy_dir')
def test_backup_system_launch_agents(copy_mock):
    source = config.get_system_launch_agents_dir()
    dest = config.get_system_launch_agents_backup_dir()
    startup_items.backup_system_launch_agents()
    copy_mock.assert_called_with(
        source, dest
    )


@patch('startup_items.copy_dir')
def test_backup_system_daemons_agents(copy_mock):
    source = config.get_system_launch_daemons_dir()
    dest = config.get_system_launch_daemons_backup_dir()
    startup_items.backup_system_daemons_agents()
    copy_mock.assert_called_with(
        source, dest
    )


@patch('startup_items.ensure_dir_owned_by_user')
@patch('startup_items.copy_dir')
def test_restore_user_launch_agents(copy_mock, owned_mock):
    source = config.get_user_launch_agents_backup_dir()
    dest = config.get_user_launch_agents_dir()
    startup_items.restore_user_launch_agents()
    copy_mock.assert_called_with(
        source, dest, with_sudo=True
    )
    owned_mock.assert_called_with(
        dest, config.get_user()
    )


@patch('startup_items.ensure_dir_owned_by_user')
@patch('startup_items.copy_dir')
def test_restore_system_launch_agents(copy_mock, owned_mock):
    source = config.get_system_launch_agents_backup_dir()
    dest = config.get_system_launch_agents_dir()
    startup_items.restore_system_launch_agents()
    copy_mock.assert_called_with(
        source, dest, with_sudo=True
    )
    owned_mock.assert_called_with(
        dest, 'root:wheel', '644'
    )


@patch('startup_items.ensure_dir_owned_by_user')
@patch('startup_items.copy_dir')
def test_restore_system_daemons_agents(copy_mock, owned_mock):
    source = config.get_system_launch_daemons_backup_dir()
    dest = config.get_system_launch_daemons_dir()
    startup_items.restore_system_daemons_agents()
    copy_mock.assert_called_with(
        source, dest, with_sudo=True
    )
    owned_mock.assert_called_with(
        dest, 'root:wheel', '644'
    )
