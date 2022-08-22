#!/usr/bin/python

import subprocess

reg = "^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\(([\w\-.]+)\))?(!)?: ([\w ])+([\s\S]*)"
msg = "\nregex rule commit message must follow, so it looks like this:\n<type>(scope optional): <description>"

repo_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
repo_dir = str(repo_dir)
nav = repo_dir+r"/.git/COMMIT_EDITMSG"
print(nav)

with open(nav, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("%s %s \n%s" % (reg, msg, content))
