#!/usr/bin/python

import sys
import re
import subprocess

ptrn = re.compile("^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\(([\w\-.]+)\))?(!)?: ([\w ])+([\s\S]*)")

repo_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
repo_dir = str(repo_dir)
nav = repo_dir+r"/.git/COMMIT_EDITMSG"
print(nav)

with open(nav, 'r+') as f:
        msg = f.readline()
        print(msg)
if not ptrn.match(msg):
    print("message doesn't follow rules")
    sys.exit(1)
