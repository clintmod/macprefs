from subprocess import CalledProcessError, check_output, STDOUT
import sys
import importlib
import logging as log


def execute_shell(command, is_shell=False, cwd='.', suppress_errors=False):
    output = ''
    log.debug('\n--- executing shell command ----\n')
    log.debug('setting working dir to: %s', cwd)
    log.debug('command: %s', str(command))
    try:
        output = check_output(command, shell=is_shell,
                              cwd=cwd, stderr=STDOUT).strip().decode('utf-8')
        log.debug('output = %s', output)
    except CalledProcessError as err:
        log.error('Error Info:\nerror code = %s\ncmd %s\nerror message:%s',
                  err.returncode, err.cmd, err.output)
        if not suppress_errors:
            raise
    finally:
        log.debug('\n---- shell execution finished ---\n')
    return output


def copy_dir(src, dest, with_sudo=False):
    extra_args = []
    if log.root.getEffectiveLevel() == log.DEBUG:
        extra_args = ['-vv']
    command = ['rsync', '-a'] + extra_args + [src, dest]
    if with_sudo:
        command = ['sudo'] + command
    execute_shell(command)


def copy_files(files, dest):
    extra_args = []
    if log.root.getEffectiveLevel() == log.DEBUG:
        extra_args = ['-vv']
    command = ['rsync', '-a'] + extra_args + files + [dest]
    execute_shell(command)


def copy_file(fle, dest):
    extra_args = []
    if log.root.getEffectiveLevel() == log.DEBUG:
        extra_args = ['-vv']
    command = ['rsync', '-a'] + extra_args + [fle, dest]
    execute_shell(command)


def ensure_dir_owned_by_user(path, user, mode='600'):
    change_mode(path, mode)
    change_owner(path, user)
    ensure_subdirs_listable(path)


def ensure_files_owned_by_user(user, files, mode='600'):
    change_mode_for_files(files, mode)
    change_owner_for_files(files, user)


def change_owner_for_files(files, user):
    command = ['sudo', 'chown', user] + files
    result = execute_shell(command)
    if not is_none_or_empty_string(result):
        log.debug(result)


def change_mode_for_files(files, mode):
    command = ['sudo', 'chmod', str(mode)] + files
    result = execute_shell(command)
    if not is_none_or_empty_string(result):
        log.debug('change_mode_for_files: %s', result)


def change_owner(path, owner, should_recurse=True):
    command = ['sudo', 'chown']
    if should_recurse:
        command += ['-R']
    command += [owner, path]
    result = execute_shell(command)
    if not is_none_or_empty_string(result):
        log.debug(result)


def change_mode(path, mode, should_recurse=True):
    command = ['sudo', 'chmod']
    if should_recurse:
        command += ['-R']
    command += [str(mode), path]
    result = execute_shell(command)
    if not is_none_or_empty_string(result):
        log.debug(result)


def ensure_subdirs_listable(path):
    command = ['sudo', 'chmod', '-R', 'a+X', path]
    result = execute_shell(command)
    if not is_none_or_empty_string(result):
        log.debug(result)


def is_none_or_empty_string(val):
    if val is None or val == '':
        return True
    return False


def execute_module(name, path):
    spec = importlib.util.spec_from_loader(name, importlib.machinery.SourceFileLoader(name, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules[name] = mod
    return mod
