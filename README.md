# Manage Git Repos

Typically, when I am working on personal projects my work flow involves a number of repos for different parts of a project. Typically I am the only one working on the repositories across different machines. I wrote this script to help me out. The script will allow me to iterate recursively through a file path and find all valid repos. I can then do batch operations such as stage all unstaged changes. Commit any stage changes and push them to remote repositories. It is really quite nice. Typically I'll have private repos stored on my home computers and have remote repos on my laptops or other systems.

I simply work on master. I don't see a reason to do anything different as I am not generally collaborating with anyone on these projects. In order to push my changes to my remote repositories I need to create a branch to push because it won't let me push to the remote repo on master.

So master contains the latest changes. When I work on another computer I work on a branch named after that computer. When I get back to my main system I merge all the branches into master. It is really quite simple. The complexity comes with the shear number of repos to manage. This is where the script comes in.


The script, given a path will recursively search for git repos. The operation will be applied to each repository in succession. You can:
- list - This will simply list the names of the repos that were found.
- status - This will list the status of each repository.
- checkout - This will create a new branch and checkout it for each repository. Typically the branch is named after the computer I am currently working on.
- add - Stage any new files to the current branch.
- commit - Commit any staged changes to the current branch.
- push - Push the staged changes to the remote repository.
- changes_to_remote - This is a group method that creates the new branch, adds any changes, commits the changes and pushes in one go for each repository.

```
$ python3 manage_repos.py --help
usage: manage_repos.py [-h] [-l] [-s] [--checkout BRANCH NAME] [--add]
                       [--commit MESSAGE] [--push] [--changes_to_remote]
                       path

Manage Git Repositories.

positional arguments:
  path                  The root path where the repos are located.

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List all of the repositories recursively from the
                        root.
  -s, --status          List the status of the repositories.
  --checkout BRANCH NAME
                        The name of the branch in the repo to checkout. It
                        will be created if it doesn't exist.
  --add                 Add new files to the stage of the current branch.
  --commit MESSAGE      Commit the files to the active branch with the commit
                        message.
  --push                Push the changes to remote, creating a tracking branch
                        if required.
  --changes_to_remote   Take the changes in a repo, create a branch, commit
                        them and push to remote creating a tracking branch if
                        necessary. Required: --checkout BRANCH NAME and
                        --commit MESSAGE
```