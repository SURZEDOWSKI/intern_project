#!/usr/bin/python
import sys
import re

ptrn = re.compile("^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\(([\w\-.]+)\))?(!)?: ([\w ])+([\s\S]*)")

with open(r"COMMIT_EDITMSG", 'r+') as f:
        msg = f.readline()
        print(msg)
        if not ptrn.match(msg):
	        print("message doesn't follow rules")
	        sys.exit(1)
