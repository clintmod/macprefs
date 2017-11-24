from subprocess import CalledProcessError, check_output, STDOUT


def execute_shell(command, is_shell=False, cwd='.', suppress_errors=False, verbose=False):
    output = ''
    if verbose:
        print '\n--- executing shell command ----\n'
        print 'setting working dir to: ' + cwd
        print 'command: ' + str(command)
    try:
        output = check_output(command, shell=is_shell,
                              cwd=cwd, stderr=STDOUT).strip()
        if verbose:
            print 'output = ' + output
    except CalledProcessError as err:
        print 'Error Info:\nerror code = {0}\ncmd {1}\nerror message: {2}'.format(err.returncode, err.cmd, err.output)
        if not suppress_errors:
            raise
    finally:
        if verbose:
            print '---- shell execution finished ---\n'
    return output


def copy_dir(src, dest, with_sudo=False):
    command = ['rsync', '-a'] + [src, dest]
    if with_sudo:
        command = ['sudo'] + command
    result = execute_shell(command)
    if not is_none_or_empty_string(result):
        print result


def copy_files(files, dest):
    command = ['rsync', '-a'] + files + [dest]
    result = execute_shell(command)
    if not is_none_or_empty_string(result):
        print result


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
        print result


def change_mode_for_files(files, mode):
    command = ['sudo', 'chmod', str(mode)] + files
    result = execute_shell(command)
    if not is_none_or_empty_string(result):
        print 'change_mode_for_files: ' + result


def change_owner(path, owner, should_recurse=True):
    command = ['sudo', 'chown']
    if should_recurse:
        command += ['-R']
    command += [owner, path]
    result = execute_shell(command)
    if not is_none_or_empty_string(result):
        print result


def change_mode(path, mode, should_recurse=True):
    command = ['sudo', 'chmod']
    if should_recurse:
        command += ['-R']
    command += [str(mode), path]
    result = execute_shell(command)
    if not is_none_or_empty_string(result):
        print result


def ensure_subdirs_listable(path):
    command = ['sudo', 'chmod', '-R', 'a+X', path]
    result = execute_shell(command)
    if not is_none_or_empty_string(result):
        print result


def is_none_or_empty_string(val):
    if val is None or val == '':
        return True
    return False