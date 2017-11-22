from subprocess import CalledProcessError, check_output, STDOUT


def execute_shell(command, is_shell=False, cwd=".", suppress_errors=False, verbose=False):
    output = ""
    if verbose:
        print "\n--- executing shell command ----\n"
        print "setting working dir to: " + cwd
        print "command: " + str(command)
    try:
        output = check_output(command, shell=is_shell,
                              cwd=cwd, stderr=STDOUT).strip()
        if verbose:
            print "output = " + output
    except CalledProcessError as err:
        print "Error Info:\nerror code = {0}\ncmd {1}\nerror message: {2}".format(err.returncode, err.cmd, err.output)
        if not suppress_errors:
            raise
    finally:
        if verbose:
            print "---- shell execution finished ---\n"
    return output


# pylint: disable-msg=too-many-arguments
def copy_files(src, dest, with_sudo=False, as_archive=True, verbose=True, extra_args=None, as_dir=False):
    main_args = []
    if extra_args is None:
        extra_args = []
    if as_archive:
        main_args += ['-a']
    if verbose:
        main_args += ['-v']
    if as_dir:
        main_args += ['-r']
    command = ['cp'] + main_args + extra_args + [src, dest]
    if with_sudo:
        command = ['sudo'] + command
    result = execute_shell(command)
    if result is not None:
        print result


def ensure_owned_by_user(path, user, mode='600'):
    change_mode(path, mode)
    change_owner(path, user)
    ensure_subdirs_listable(path)


def change_owner(path, owner, should_recurse=True):
    command = ['sudo', 'chown']
    if should_recurse:
        command += ['-R']
    command += [owner, path]
    result = execute_shell(command)
    if result is not None:
        print result


def change_mode(path, mode, should_recurse=True):
    command = ['sudo', 'chmod']
    if should_recurse:
        command += ['-R']
    command += [str(mode), path]
    result = execute_shell(command)
    if result is not None:
        print result


def ensure_subdirs_listable(path):
    command = ['sudo', 'chmod', '-R', 'a+X', path]
    result = execute_shell(command)
    if result is not None:
        print result
