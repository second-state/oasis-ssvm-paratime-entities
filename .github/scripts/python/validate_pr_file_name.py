#!/usr/bin/env python3
import os
import sys
from github import Github

class InvalidPR(Exception):
    pass

def get_expected_filename(filename, pr_creator):
    expected_testnet_filename = "testnet/%s-entity.json" % pr_creator
    expected_mainnet_filename = "mainnet/%s-entity.json" % pr_creator

    if (filename == expected_mainnet_filename):
        print('Submit mainnet entity %s ', filename)
        return 'mainnet'
    elif (filename == expected_testnet_filename):
        print('Submit testnet entity %s ', filename)
        return 'testnet'
    else:
        raise InvalidPR(
            'The entity file is expected to be named %s or %s. Your filename is %s Please rename it' % (expected_testnet_filename, expected_mainnet_filename, filename)
        )


def validate_pull_request(gh, repo, pr_number):
    """Validate if this pull request is a valid pull request."""
    repo = gh.get_repo(repo)
    pr = repo.get_pull(pr_number)
    pr_creator = pr.user.login

    is_valid = False

    changed_files = list(pr.get_files())
    if len(changed_files) > 2:
        raise InvalidPR(
            'This PR contains too many entity changes. That is not allowed without explicit review.'
        )

    for changed_file in changed_files:
        _ = get_expected_filename(changed_file.filename, pr_creator)


def main():
    token = os.environ.get('GITHUB_TOKEN')
    github_ref = os.environ.get('GITHUB_REF', '')
    if not token:
        print('No github token specified')
        sys.exit(1)
    if not github_ref:
        print('No github_ref specified')
        sys.exit(1)

    try:
        pr_number = int(github_ref.split('/')[2])
    except TypeError:
        print("This is not a PR")
        sys.exit(1)

    gh = Github(token)

    print("Validating PR #%d" % pr_number)

    try:
        validate_pull_request(
            gh,
            'second-state/oasis-ssvm-paratime-entities',
            pr_number
        )
    except InvalidPR as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
