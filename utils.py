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
        output = err.output
        # when the check_output raises an error, it also stores the result as bytes.
        if isinstance(output, bytes):
            output = output.decode('ascii')
        if not suppress_errors:
            raise
    finally:
        log.debug('\n---- shell execution finished ---\n')
    return output


def restart_cfprefsd():
    # cfprefsd caches preferences in memory and will clobber freshly restored
    # .plist files with its stale cache. Killing it forces launchd to relaunch
    # it on demand so restored preferences are picked up. killall exits nonzero
    # when no process matches, which is harmless here, so suppress errors.
    execute_shell(['sudo', 'killall', 'cfprefsd'], suppress_errors=True)


def run_rsync(command):
    # rsync exits 23 (partial transfer) / 24 (some files vanished) when a few
    # files can't be read/copied -- e.g. plists owned by security tools in
    # /Library/LaunchDaemons. Copying everything else is far more useful than
    # aborting the whole backup/restore, so warn and continue on those codes.
    try:
        execute_shell(command)
    except CalledProcessError as err:
        if err.returncode in (23, 24):
            log.warning('rsync partial transfer (exit %s): %s',
                        err.returncode, err.output)
        else:
            raise


def copy_dir(src, dest, with_sudo=False):
    extra_args = []
    if log.root.getEffectiveLevel() == log.DEBUG:
        extra_args = ['-vv']
    command = ['rsync', '-a'] + extra_args + [src, dest]
    if with_sudo:
        command = ['sudo'] + command
    run_rsync(command)


def copy_files(files, dest):
    extra_args = []
    if log.root.getEffectiveLevel() == log.DEBUG:
        extra_args = ['-vv']
    command = ['rsync', '-a'] + extra_args + files + [dest]
    run_rsync(command)


def copy_file(fle, dest):
    extra_args = []
    if log.root.getEffectiveLevel() == log.DEBUG:
        extra_args = ['-vv']
    command = ['rsync', '-a'] + extra_args + [fle, dest]
    run_rsync(command)


def ensure_dir_owned_by_user(path, user, mode='600'):
    change_mode(path, mode)
    change_owner(path, user)
    ensure_subdirs_listable(path)


def ensure_files_owned_by_user(user, files, mode='600'):
    change_mode_for_files(files, mode)
    change_owner_for_files(files, user)


def run_permission_change(command):
    # chown/chmod are rejected on files protected by security tools (SIP,
    # endpoint agents). One protected file shouldn't abort a whole restore, so
    # suppress the error and warn -- restoring everything else still succeeds.
    result = execute_shell(command, suppress_errors=True)
    if not is_none_or_empty_string(result):
        log.warning('permission change failed: %s', result)


def change_owner_for_files(files, user):
    command = ['sudo', 'chown', user] + files
    run_permission_change(command)


def change_mode_for_files(files, mode):
    command = ['sudo', 'chmod', str(mode)] + files
    run_permission_change(command)


def change_owner(path, owner, should_recurse=True):
    command = ['sudo', 'chown']
    if should_recurse:
        command += ['-R']
    command += [owner, path]
    run_permission_change(command)


def change_mode(path, mode, should_recurse=True):
    command = ['sudo', 'chmod']
    if should_recurse:
        command += ['-R']
    command += [str(mode), path]
    run_permission_change(command)


def ensure_subdirs_listable(path):
    command = ['sudo', 'chmod', '-R', 'a+X', path]
    run_permission_change(command)


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
