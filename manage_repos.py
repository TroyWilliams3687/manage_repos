#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""

This script will assist in managing a large number of repositories where there
is only one author or contributor.

TODO

add an option to do the following on my home computer:
$ git merge LT-IRI-01 <- cli option
$ git branch -d LT-IRI-01 <- CLI option - this may not be necessary as I may just leave it in


# -------------------------
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


def run_counter_command(command, repo_path):
    """
    Takes the list and attempts to run it in the command shell. Returns a Counter indicating the status.

    Note: all bits of the command and parameter must be a separate entry in the
    list.
    """
    if not command:
        raise Exception("Valid command required - fill the list please!")

    p = Popen(command, stdout=PIPE, shell=False, cwd=repo_path)
    retval = p.wait()

    if retval != 0:
        raise ValueError("Something happened while running the command!")

    status = Counter(line.decode("utf-8").split()[0] for line in p.stdout)

    return status


def run_command(command, repo_path):
    """
    Takes the list and attempts to run it in the command shell.

    Note: all bits of the command and parameter must be a separate entry in the
    list.
    """
    if not command:
        raise Exception("Valid command required - fill the list please!")

    p = Popen(command, stdout=PIPE, shell=False, cwd=repo_path)
    retval = p.wait()

    status = [line.decode("utf-8") for line in p.stdout]

    return retval, status


def create_argument_parser():
    """
    """

    parser = argparse.ArgumentParser(description="Manage Git Repositories.")
    parser.add_argument(
        "path", help="The root path where the repos are located.", default=Path.cwd()
    )

    parser.add_argument(
        "-l",
        "--list",
        help="List all of the repositories recursively from the root.",
        action="store_true",
    )

    parser.add_argument(
        "-s",
        "--status",
        help="List the status of the repositories.",
        action="store_true",
    )

    parser.add_argument(
        "--status-remote",
        help="List the status of the repositories compared to the remotes.",
        action="store_true",
    )

    parser.add_argument(
        "--checkout",
        help="The name of the branch in the repo to checkout. It will be created if it doesn't exist.",
        action="store",
        default=None,
        metavar="BRANCH NAME",
    )

    parser.add_argument(
        "--add",
        help="Add new files to the stage of the current branch.",
        action="store_true",
    )

    parser.add_argument(
        "--commit",
        help="Commit the files to the active branch with the commit message.",
        action="store",
        default=None,
        metavar="MESSAGE",
    )

    parser.add_argument(
        "--push",
        help="Push the changes to remote, creating a tracking branch if required.",
        action="store_true",
    )

    parser.add_argument(
        "--pull",
        help="Pull the changes from remote and merging the active branch.",
        action="store_true",
    )

    parser.add_argument(
        "--fetch-all",
        help="Fetch all changes for all branches from the remote.",
        action="store_true",
    )

    parser.add_argument(
        "--changes_to_remote",
        help="Take the changes in a repo, create a branch, commit them and push to remote creating a tracking branch if necessary. Required: --checkout BRANCH NAME and --commit MESSAGE",
        action="store_true",
    )

    return parser


def unstaged_changes(repo):
    """
    If there are unstaged changes in the repository, this method returns True.
    """

    # We can check for unstaged changes with:
    git = ["git", "diff", "--exit-code"]
    retval, status = run_command(git, repo)

    return retval == 0


def staged_changes(repo):
    """
    If there are staged changes, but not committed, this method will return true.
    """

    # To check if there are any changes that are staged but not committed
    git = ["git", "diff", "--cached", "--exit-code"]
    retval, status = run_command(git, repo)
    return retval == 0


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


def display_status(repo):
    """
    """
    # https://codereview.stackexchange.com/questions/117639/bash-function-to-parse-git-status
    # https://stackoverflow.com/questions/30449862/is-there-a-method-of-getting-the-number-of-files-in-git-repository-with-new-modi
    # https://unix.stackexchange.com/questions/155046/determine-if-git-working-directory-is-clean-from-a-script

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

    git = ["git", "status", "--porcelain"]
    status = run_counter_command(git, repo)

    if len(status) == 0:
        print(f"{repo} - no changes...")
        return

    print(repo)
    if "??" in status:
        print("\tUntracked: {}".format(status["??"]))

    if "M" in status:
        print("\tModified:  {}".format(status["M"]))

    if "D" in status:
        print("\tDeleted:   {}".format(status["D"]))

    if "A" in status:
        print("\tAdded:     {}".format(status["A"]))

    if "R" in status:
        print("\tRenamed:   {}".format(status["R"]))

    if "C" in status:
        print("\tCopied:    {}".format(status["C"]))

    if "U" in status:
        print("\tUnmerged:  {}".format(status["U"]))

    status_codes = set(("??", "M", "D", "A", "R", "C", "U"))
    counter_keys = set(status.keys())

    # See if there are any returned keys in the counter that we don't account for
    missing_keys = counter_keys.difference(status_codes)

    for k in missing_keys:
        print(f"{k} = {status[k]}")


def checkout(repo, branch):
    """
    Switch to the list branch updating the files in the working tree to match the
    version in the branch.

    If the branch doesn't exist it will be created.
    """

    # check to see if the branch is active, if it is we don't need to check it out
    git = ["git", "branch"]
    retval, status = run_command(git, repo)

    for b in status:
        if b.strip().startswith("*"):
            if b[1:].strip().lower() == branch.lower():
                return [f"{branch} Already Checked out..."]

    git = ["git", "checkout", "-b", branch]
    retval, status = run_command(git, repo)

    if retval != 0:
        print("\n".join(status))
        print()
        raise ValueError("Something happened while running the git checkout!")

    return status


def add(repo):
    """
    Add all new files to the stage of the current branch
    """

    if unstaged_changes(repo):
        return ["No unstaged changes to add..."]

    git = ["git", "add", "."]
    retval, status = run_command(git, repo)

    if retval != 0:
        print("\n".join(status))
        print()
        raise ValueError("Something happened while running the git add!")

    return status


def commit(repo, msg):
    """
    commit all staged files to the current branch
    """

    if staged_changes(repo):
        return ["No stagged changes to commit..."]

    # there are stagged changes that need to be committed
    git = ["git", "commit", "-a", "-m", msg]
    retval, status = run_command(git, repo)

    if retval != 0:
        print("\n".join(status))
        print()
        raise ValueError("Something happened while running the git commit!")

    return status


def push(repo):
    """
    push the branch to remote creating a tracker in the remote if necessary

    -u; --set-upstream - For every branch that is up to date or successfully
    pushed, add upstream (tracking) reference, used by argument-less
    git-pull[1] and other commands.

    --all - Push all branches (i.e. refs under refs/heads/); cannot be
    used with other <refspec>.
    """

    # git = ["git", "push", "--porcelain", "-u", "--all"]
    git = ["git", "push", "--set-upstream", "--all"]

    retval, status = run_command(git, repo)

    if retval != 0:
        print("\n".join(status))
        print()
        raise ValueError("Something happened while running the git push!")

    return status

def pull(repo):
    """
    Pull changes from remote to the active branch and merge the changes locally.
    """

    # The ssh key needs to be stored in a key agent otherwise the password
    # prompt will kill the script

    git = ["git", "pull"]

    retval, status = run_command(git, repo)

    if retval != 0:
        print("\n".join(status))
        print()
        raise ValueError("Something happened while running the git pull!")

    return status

def fetch_all(repo):
    """
    Fetch all changes from remote.
    """

    # The ssh key needs to be stored in a key agent otherwise the password
    # prompt will kill the script

    print(repo)

    git = ["git", "fetch", "--all"]

    retval, status = run_command(git, repo)

    if retval != 0:
        print("\n".join(status))
        print()
        raise ValueError("Something happened while running the git fetch --all!")

    return status

def status_remote(repo):
    """
    The idea is to check to see if there are changes in the remote repo and if
    so what is the state.
    """

    # how to check to see if a repo needs to be updated with a remote:
    # https://stackoverflow.com/questions/3258243/check-if-pull-needed-in-git

    # $ git remote -v update
    # Fetching origin
    # Enter passphrase for key 'D:\documents\home\.ssh\id_rsa':
    # remote: Counting objects: 7, done.
    # remote: Compressing objects: 100% (5/5), done.
    # remote: Total 7 (delta 1), reused 0 (delta 0)
    # Unpacking objects: 100% (7/7), done.
    # From ssh://bluebill.strangled.net:10000/mnt/backup/repositories/jupyter/projects
    #    f497f5c..b4b8e9a  master     -> origin/master
    #  = [up to date]      LT-IRI-01  -> origin/LT-IRI-01

    # in the above, the remote is ahead of the master branch of the local repo.
    # This means that we can pull the changes

    print(repo)

    git = ["git", "remote", "-v", "update"]

    retval, status = run_command(git, repo)

    if retval != 0:
        print("\n".join(status))
        print()
        raise ValueError("Something happened while running the git remote -v update!")

    return status


def sync_remote(repo):
    """
    Check to see if the remote is ahead of the local and pull the changes on the
    activate branch, that is the master branch locally is behind the remote.

    """

    # how to check to see if a repo needs to be updated with a remote:
    # https://stackoverflow.com/questions/3258243/check-if-pull-needed-in-git

    # $ git remote -v update
    # Fetching origin
    # Enter passphrase for key 'D:\documents\home\.ssh\id_rsa':
    # remote: Counting objects: 7, done.
    # remote: Compressing objects: 100% (5/5), done.
    # remote: Total 7 (delta 1), reused 0 (delta 0)
    # Unpacking objects: 100% (7/7), done.
    # From ssh://bluebill.strangled.net:10000/mnt/backup/repositories/jupyter/projects
    #    f497f5c..b4b8e9a  master     -> origin/master
    #  = [up to date]      LT-IRI-01  -> origin/LT-IRI-01

    # in the above, the remote is ahead of the master branch of the local repo.
    # This means that we can pull the changes

    # $ git pull
    # Enter passphrase for key 'D:\documents\home\.ssh\id_rsa':
    # Updating f497f5c..b4b8e9a
    # Fast-forward
    #  blood pressure/blood pressure.ipynb        | 1276 ++++++++++++++++++++++++++++
    #  blood pressure/data/raw/blood_pressure.csv |   67 ++
    #  2 files changed, 1343 insertions(+)
    #  create mode 100644 blood pressure/blood pressure.ipynb
    #  create mode 100644 blood pressure/data/raw/blood_pressure.csv

    # $ git remote -v update
    # Fetching origin
    # Enter passphrase for key 'D:\documents\home\.ssh\id_rsa':
    # From ssh://bluebill.strangled.net:10000/mnt/backup/repositories/jupyter/projects
    #  = [up to date]      master     -> origin/master
    #  = [up to date]      LT-IRI-01  -> origin/LT-IRI-01

    pass



def changes_to_remote(repo, branch_name, commit_msg):
    """
    Checkout the branch (creates it if it doesn't exist), adds all new files to the stage,
    commits the changes using the commit message and finally pushes the changes to the remote
    creating the proper tracking branches.

    This is used in my workflow where I have a number of repos across different computers. The latest
    will always be on master

    Parameters
    ----------
    repo - Path - path to the repository
    branch_name - str - The name of the branch to use or create. This should be unique to the remote computers
    commit_msg - str - The message used when committing the changes. This will probably be generic.

    """

    print("Checkout...")
    status = checkout(repo, branch_name)
    print("\n".join(status))
    print()

    print("Add...")
    status = add(repo)
    print("\n".join(status))
    print()

    print("Commit...")
    status = commit(repo, commit_msg)
    print("\n".join(status))
    print()

    print("Push...")
    status = push(repo)
    print("\n".join(status))
    print()


def main():
    """
    This runs the rest of the functions in this module
    """

    parser = create_argument_parser()
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        raise ValueError(f"{args.path} doesn't exist!")

    if not root.is_dir():
        raise ValueError(f"{args.path} is not a directory!")

    print("Searching for repos...")
    repos = find_repos(root) # could convert this into a generator

    # could deal with this list of options better, no point in searching for
    # repos if non of the arguments are set

    if args.list:
        for r in repos:
            print(r)

    elif args.status:
        for r in repos:
            display_status(r)

    elif args.status_remote:
        for r in repos:
            status_remote(r)

    elif args.add:
        for r in repos:
            status = add(r)
            print("\n".join(status))

    elif args.pull:
        for r in repos:
            status = pull(r)
            print("\n".join(status))

    elif args.push:
        for r in repos:
            status = push(r)
            print("\n".join(status))

    elif args.fetch_all:
        for r in repos:
            status = fetch_all(r)
            print("\n".join(status))

    elif args.changes_to_remote:
        # this has to be before --checkout and --commit

        if args.checkout is None or args.commit is None:
            print("--checkout and --commit are required!")
            print()
            parser.print_help()

            return 1

        for r in repos:
            changes_to_remote(r, args.checkout, args.commit)

    elif args.checkout:

        for r in repos:
            status = checkout(r, args.checkout)
            print("\n".join(status))

    elif args.commit:
        for r in repos:
            status = commit(r, args.commit)
            print("\n".join(status))

    else:
        print("No option specified...")

    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
