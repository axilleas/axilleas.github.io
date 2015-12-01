import os
import time

from fabric.api import local, lcd, settings
from fabric.utils import puts

#If no local_settings.py then settings.py
from settings_dev import OUTPUT_PATH
SETTINGS_FILE = "settings_prod.py"
SETTINGS_DEV_FILE = "settings_dev.py"


# Get directories
ABS_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_SETTINGS_FILE = os.path.join(ABS_ROOT_DIR, SETTINGS_FILE)
ABS_SETTINGS_DEV_FILE = os.path.join(ABS_ROOT_DIR, SETTINGS_DEV_FILE)
ABS_OUTPUT_PATH = os.path.join(ABS_ROOT_DIR, OUTPUT_PATH)


# Commands
def venv():
    """Change virtualenv"""

    cmd = "source $HOME/Venvs/pelican-py2/bin/activate"

    local(cmd)

def generate(output=None):
    """Generates the pelican static site"""

    if not output:
        cmd = "pelican -s {0}".format(ABS_SETTINGS_FILE)
    else:
        cmd = "pelican -s {0} -o {1}".format(ABS_SETTINGS_FILE, output)

    local(cmd)

def dev():
    """Generated site on the fly with each change"""

    cmd = "pelican -s {0} -d -r --ignore-cache".format(ABS_SETTINGS_DEV_FILE)

    local(cmd)

def destroy(output=None):
    """Destroys the pelican static site"""

    if not output:
        cmd = "rm -r {0}".format(os.path.join(ABS_ROOT_DIR, OUTPUT_PATH))
    else:
        cmd = "rm -r {0}".format(output)

    with settings(warn_only=True):
        result = local(cmd)
    if result.failed:
        puts("Already deleted")


def serve():
    """Serves the site in the development webserver"""
    print(ABS_OUTPUT_PATH)
    with lcd(ABS_OUTPUT_PATH):
        local("python2 -m SimpleHTTPServer")


def git_change_branch(branch):
    """Changes from one branch to other in a git repo"""
    local("git checkout {0}".format(branch))


def git_merge_branch(branch):
    """Merges a branch in other branch"""
    local("git merge {0}".format(branch))

def git_checkout_branch():
    """Checkouts the src/ of the source branch into master (must be in master)"""
    local("git checkout source -- src")

def git_push(remote, branch):
    """Pushes the git changes to git remote repo"""
    local("git push {0} {1}".format(remote, branch))

def git_commit_all(msg):
    """Commits all the changes"""
    local("git add .")
    local("git commit -m \"{0}\"".format(msg))

def publish():
    """Generates and publish the new site in github pages"""
    source_branch = "source"
    publish_branch = "master"
    remote = "origin"

    # Push original changes to source
    git_push(remote, source_branch)

    # Change to master branch
    git_change_branch(publish_branch)

    # Merge master into source
    git_checkout_branch()

    # Generate the html
    generate(ABS_ROOT_DIR)

    # Commit changes
    now = time.strftime("%d %b %Y %H:%M:%S", time.localtime())
    git_commit_all("Publication {0}".format(now))

    # Push to gh-pages branch
    git_push(remote, publish_branch)

    # go to master
    git_change_branch(source_branch)
