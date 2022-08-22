#!/usr/bin/python

import sys
import re
import subprocess
import argparse

def onPreReceive(oldrev, newrev, refname):

    refname = refname.strip()
    refname = refname.removeprefix('refs/heads/')
    ptrn = re.compile("^b'(major|feature|bugfix|hotfix)\/*")

    if not ptrn.match(refname):
       print("Wrong branch name!")
       sys.exit(1)
    else:
        proc = subprocess.Popen(['git', 'rev-list','--oneline','--first-parent'], stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        if lines:
            rev = str(lines[0])
            ptrn2 = re.compile("^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\(([\w\-.]+)\))?(!)?: ([\w ])+([\s\S]*)")
            if not ptrn2.match(rev):
                print("Wrong commit message!")
                exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('oldrev', help='old object name stored in the ref')
parser.add_argument('newrev', help='new object name stored in the ref')
parser.add_argument('refname', help='full name of the ref')

for line in sys.stdin:
    args = parser.parse_args(line.strip().split(' '))
    onPreReceive(args.oldrev, args.newrev, args.refname)
