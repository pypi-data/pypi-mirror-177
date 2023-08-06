# -*- coding: utf-8 -*-

"""
Definition of constants and helper functions shared by all scripts
"""

import os
import re

from hito_tools.core import is_windows

from .exceptions import (
    GitCommitHashNotUnique,
    GitCommitNotFound,
    GitPythonModuleMissing,
    GitRepoNotFound,
)

try:
    from git import Repo

    GITPYTHON_AVAILABLE = True
except Exception:
    GITPYTHON_AVAILABLE = False


def get_commit(repo, commit_hash):
    commit_list = [c for c in repo.iter_commits() if re.match("{}.*".format(commit_hash), c.hexsha)]
    if len(commit_list) == 1:
        return commit_list[0]
    elif len(commit_list) == 0:
        raise GitCommitNotFound(commit_hash)
    else:
        raise GitCommitHashNotUnique(commit_hash)


def lower_if_windows(string):
    if is_windows():
        return string.lower()
    else:
        return string


def normalize_name(name, listname=True):
    if listname:
        name = name.lower()
    name = name.replace(" ", "_")
    name = name.replace("'", "_")

    return name


def open_git_repo(filename):
    """
    Open a Git repository whose path is specified through one of the filename it contains. Loops
    through the directory parents until the repository is found.

    :param filename:
    :return:
    """

    if not GITPYTHON_AVAILABLE:
        raise GitPythonModuleMissing

    current_path = os.path.dirname(os.path.abspath(filename))
    previous_path = ""
    git_repo = None

    while current_path != previous_path and not git_repo:
        try:
            git_repo = Repo(current_path)
        except Exception:
            previous_path = current_path
            current_path = os.path.dirname(current_path)

    if git_repo:
        return git_repo
    else:
        raise GitRepoNotFound(filename)
