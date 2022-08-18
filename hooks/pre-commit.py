#!/usr/bin/python

import subprocess
import sys
import re

def branch_name():
	bashCommand = "git rev-parse --abbrev-ref HEAD"
	process = subprocess.check_output(bashCommand)
	return process

branch = str(branch_name())

ptrn = re.compile("^b'(major|feature|bugfix|hotfix)\/*")

if ptrn.match(branch):
	print(branch, " fits pattern")
else:
	print("wrong branch name")
	sys.exit(0)