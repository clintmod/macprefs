from subprocess import CalledProcessError, check_output, STDOUT


def execute_shell(command, is_shell=False, cwd=".", suppress_errors=False, verbose=False):
    output = ""
    if verbose:
        print "\n--- executing shell command ----\n"
        print "setting working dir to: " + cwd
        print "command: " + str(command)
    if 'cp' in command and not '-a' in command:
        raise ValueError('cp requires -a')
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
