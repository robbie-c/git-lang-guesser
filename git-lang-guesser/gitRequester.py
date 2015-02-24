import http.client

import requests

from . import exceptions

USER_URL = 'https://api.github.com/users/{username}'
USER_PUBLIC_REPO_URL = 'https://api.github.com/users/{username}/repos'


def do_request(url_format, format_args):
    r = requests.get(url_format.format(**format_args))

    if r.status_code == http.client.OK:
        return r.json()
    else:
        raise exceptions.RequestFailed(r)


def get_user(username):
    return do_request(USER_URL, {"username": username})


def get_public_projects_for_user(username):
    return do_request(USER_PUBLIC_REPO_URL, {"username": username})


if __name__ == "__main__":
    import pprint
    pprint.pprint(get_user("robbie-c"))
    pprint.pprint(get_public_projects_for_user("robbie-c"))
