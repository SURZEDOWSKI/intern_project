#!/usr/bin/python

import subprocess
import sys
import re

branch = subprocess.check_output(['git', 'symbolic-ref', '--short', 'HEAD']).strip()
branch = str(branch)

ptrn = re.compile("^b'(major|feature|bugfix|hotfix)\/*")

if not ptrn.match(branch):
	print(branch, "doesn't follow branch naming rules")
	sys.exit(1)	