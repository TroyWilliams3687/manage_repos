#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""

This script will manage multiple git repositories

https://stackoverflow.com/questions/1456269/python-git-module-experiences

Copyright (c) 2019 Troy Williams

License: The MIT License (http://www.opensource.org/licenses/mit-license.php)
"""

# Constants
__uuid__ = ""
__author__ = "Troy Williams"
__email__ = "troy.williams@bluebill.net"
__copyright__ = "Copyright (c) 2019, Troy Williams"
__date__ = "2019-10-12"
__maintainer__ = "Troy Williams"

import sys
import argparse

from subprocess import PIPE, Popen
from collections import Counter
from pathlib import Path


def run_command(command, repo_path):
    """
    Takes the list and attempts to run it in the command shell.

    Note: all bits of the command and parameter must be a separate entry in the
    list.
    """
    if not command:
        raise Exception("Valid command required - fill the list please!")

    # p = Popen(command, shell=False, cwd=repo_path)
    # retval = p.wait()

    # return status

    p = Popen(command, stdout=PIPE, shell=False, cwd=repo_path)
    retval = p.wait()

    if retval != 0:
        raise ValueError("Something happened while running the command!")

    status = Counter(line.decode("utf-8").split()[0] for line in p.stdout)

    return status

    # pipe = Popen(command, stdout=PIPE, cwd=repo_path)
    # status = Counter(line.split()[0] for line in pipe.stdout)

    # return status

    # pipe = subprocess.Popen(command, shell=True,
    #                                  cwd=repo_path,
    #                                  stdout = subprocess.PIPE,
    #                                  stderr = subprocess.PIPE)

    # out, error = pipe.communicate()
    # pipe.wait()

    # return

def create_argument_parser():
    """
    """

    parser = argparse.ArgumentParser(
        description="Manage Git Repositories."
    )
    parser.add_argument(
        "path",
        help="The root path where the repos are located.",
        default=Path.cwd(),
    )

    parser.add_argument("-l", "--list", help="List all of the repositories recursively from the root."
                                      , action='store_true'
                                      , default=False)

    parser.add_argument("-s", "--status", help="List the status of the repositories."
                                        , action='store_true'
                                        , default=False)

    return parser.parse_args()

def find_repos(root):
    """
    Search for all the git repos under the root folder. It will return a list
    of git repos that are relative to the root (including the root folder)

    """

    repos = []

    for f in root.rglob("*.*"):
        if f.is_dir() and f.stem == ".git":
            repos.append(f.parent)

    return repos

# def gitAdd(fileName, repoDir):
#     cmd = 'git add ' + fileName
#     pipe = subprocess.Popen(cmd, shell=True, cwd=repoDir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
#     (out, error) = pipe.communicate()
#     print out,error
#     pipe.wait()
#     return

# def gitCommit(commitMessage, repoDir):
#     cmd = 'git commit -am "%s"'%commitMessage
#     pipe = subprocess.Popen(cmd, shell=True, cwd=repoDir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
#     (out, error) = pipe.communicate()
#     print out,error
#     pipe.wait()
#     return
# def gitPush(repoDir):
#     cmd = 'git push '
#     pipe = subprocess.Popen(cmd, shell=True, cwd=repoDir,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
#     (out, error) = pipe.communicate()
#     pipe.wait()
#     return

# def command(x):
#     return str(Popen(x.split(' '), stdout=PIPE).communicate()[0])

# def rm_empty(L): return [l for l in L if (l and l!="")]

# def getUntracked():
#     os.chdir(repoDir)
#     status = command("git status")
#     if "# Untracked files:" in status:
#         untf = status.split("# Untracked files:")[1][1:].split("\n")
#         return rm_empty([x[2:] for x in untf if string.strip(x) != "#" and x.startswith("#\t")])
#     else:
#         return []

# def getNew():
#     os.chdir(repoDir)
#     status = command("git status").split("\n")
#     return [x[14:] for x in status if x.startswith("#\tnew file:   ")]

# def getModified():
#     os.chdir(repoDir)
#     status = command("git status").split("\n")
#     return [x[14:] for x in status if x.startswith("#\tmodified:   ")]

# print("Untracked:")
# print( getUntracked() )
# print("New:")
# print( getNew() )
# print("Modified:")
# print( getModified() )


def git_commands(command):
    """

    """
    git_commands = {}

    # Use git status --porcelain for this --porcelain: Give the output in a stable, easy-to-parse format for scripts... – estani Nov 5 '12 at 10:52
    # Or even better, use --z instead of --porcelain. Unlike --porcelain, --z doesn't escape filenames. – Vojislav Stojkovic Nov 12 '12 at 20:03
    # git_commands['status'] = ['git', 'status', '--z']
    git_commands['status'] = ['git', 'status', '--porcelain']

    return git_commands[command]

def display_status(repo, status):
    """
    """
    # https://codereview.stackexchange.com/questions/117639/bash-function-to-parse-git-status
    # https://stackoverflow.com/questions/30449862/is-there-a-method-of-getting-the-number-of-files-in-git-repository-with-new-modi

    # https://mirrors.edge.kernel.org/pub/software/scm/git/docs/git-status.html#_porcelain_format

    # ' ' = unmodified
    # M = modified
    # A = added
    # D = deleted
    # R = renamed
    # C = copied
    # U = updated but unmerged

    # Ignored files are not listed, unless --ignored option is in effect, in which case XY are !!.

    # X          Y     Meaning
    # -------------------------------------------------
    #          [AMD]   not updated
    # M        [ MD]   updated in index
    # A        [ MD]   added to index
    # D                deleted from index
    # R        [ MD]   renamed in index
    # C        [ MD]   copied in index
    # [MARC]           index and work tree matches
    # [ MARC]     M    work tree changed since index
    # [ MARC]     D    deleted in work tree
    # [ D]        R    renamed in work tree
    # [ D]        C    copied in work tree
    # -------------------------------------------------
    # D           D    unmerged, both deleted
    # A           U    unmerged, added by us
    # U           D    unmerged, deleted by them
    # U           A    unmerged, added by them
    # D           U    unmerged, deleted by us
    # A           A    unmerged, both added
    # U           U    unmerged, both modified
    # -------------------------------------------------
    # ?           ?    untracked
    # !           !    ignored
    # -------------------------------------------------

    print(repo)
    if '??' in status:
        print('\tUntracked: {}'.format(status['??']))

    if 'M' in status:
        print('\tModified:  {}'.format(status['M']))

    if 'D' in status:
        print('\tDeleted:   {}'.format(status['D']))

    if 'A' in status:
        print('\tAdded:     {}'.format(status['A']))

    if 'R' in status:
        print('\tRenamed:   {}'.format(status['R']))

    if 'C' in status:
        print('\tCopied:    {}'.format(status['C']))

    if 'U' in status:
        print('\tUnmerged:  {}'.format(status['U']))

    status_codes = set(('??', 'M', 'D', 'A', 'R', 'C', 'U'))
    counter_keys = set(status.keys())

    # See if there are any returned keys in the counter that we don't account for
    missing_keys = counter_keys.difference(status_codes)

    for k in missing_keys:
        print(f'{k} = {status[k]}')



def main():
    """
    This runs the rest of the functions in this module
    """

    args = create_argument_parser()

    root = Path(args.path)
    if not root.exists():
        raise ValueError(f"{args.path} doesn't exist!")

    if not root.is_dir():
        raise ValueError(f"{args.path} is not a directory!")

    print('Searching for repos...')
    repos = find_repos(root)

    if args.list:

        print(f'Found {len(repos)}...')
        for r in repos:
            print(r)

    elif args.status:

        # untracked
        # new
        # modified
        git = git_commands('status')

        for r in repos:
            status = run_command(git, r)

            if len(status) > 0:
                display_status(r, status)
                print()

            else:
                print(f'{r} - no changes...')

    else:
        print('No option specified...')


    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)