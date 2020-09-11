#!/usr/bin/env python3

# a simple way to make public issues private so people can report any issues to us in private

import os
import sys
import re
import hashlib
import time

import sh
from github import Github

def getenv(name):
    val = os.environ.get(name)
    if val == None:
        raise ValueError(f'No such environment variable: {name}')
    return val

def run():
    # pull our repo access
    src_repo = Github(getenv('SRC_REPO_TOKEN')).get_repo(getenv('GITHUB_REPOSITORY'))
    dst_repo = Github(getenv('DST_REPO_TOKEN')).get_repo(getenv('DST_REPO')) # bounce to ekoparty-internal

    # pull the src issue
    src_issue_id = int(getenv('SRC_REPO_ISSUE'))
    src_issue = src_repo.get_issue(src_issue_id)

    # bounce a comment back to the src issue
    src_issue.create_comment('Thank you for submitting a staff report! This issue will be filed to the internal ekoparty2020 staff repo and triaged ASAP!')

    # bounce the issue through to the internal repo
    dst_repo.create_issue(title=src_issue.title, body=src_issue.body, labels=[dst_repo.get_label('Staff Report')])

    # update the source issue title and make contents private
    src_issue.edit(title="This issue has been filed with staff internal repo! Thanks!", body='', state='closed')

    return 0

try:
    sys.exit(run())
except Exception as e:
    print("Error: {0}".format(e))
    sys.exit(1)
