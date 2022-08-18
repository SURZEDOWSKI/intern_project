#!/usr/bin/python
reg = "^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\(([\w\-.]+)\))?(!)?: ([\w ])+([\s\S]*)"
msg = "\nregex rule commit message must follow, so it looks like this:\n<type>(scope optional): <description>"

'''with open(r"COMMIT_EDITMSG", 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("%s %s \n%s" % (reg, msg, content))'''
