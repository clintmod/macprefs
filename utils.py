from subprocess import CalledProcessError, check_output, STDOUT

def executeShell(command, cwd = ".", suppress_errors=False, verbose = False):
	output = ""
	if(verbose):
		print "\n--- executing shell command ----\n"
		print "setting working dir to: " + cwd
		print "command: " + command
	try:
		output = check_output(command, shell=(verbose), cwd=cwd, stderr=STDOUT).strip()
		if(verbose):
			print "output = " + output
	except CalledProcessError as e:
		print "Error Info:\nerror code = {0}\ncmd {1}\nerror message: {2}".format(e.returncode, e.cmd, e.output)
		if (suppress_errors == False): raise
	finally:
		if(verbose):
			print "---- shell execution finished ---\n" 
	return output