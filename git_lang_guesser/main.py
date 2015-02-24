
import argparse
import http.client
import pprint

from . import exceptions
from . import git_requester
from . import guess_lang


def do_guess(username, list_all):
    try:
        repos = git_requester.get_public_repos_for_user(username)
    except exceptions.RequestFailed as exc:
        if exc.response.status_code == http.client.NOT_FOUND:
            print("User {0} not found".format(username))
            exit(1)
        else:
            print("HTTP error code {0}: {1}".format(exc.response.status_code, exc.response.text))
            exit(1)
        repos = []  # silence PyCharm warning

    if not repos:
        print("User does not have any public repos")
        exit(1)

    if list_all:
        counter = guess_lang.count_languages(repos, filter_none=False)
        pprint.pprint(dict(counter))
    else:
        favourite = guess_lang.guess_favourite(repos)
        print(favourite)


def main():
    parser = argparse.ArgumentParser("git_lang_guesser")
    parser.add_argument("username")
    parser.add_argument("--list-all", action="store_true")

    args = parser.parse_args()
    username = args.username
    list_all = args.list_all

    do_guess(username, list_all)


if __name__ == "__main__":
    main()