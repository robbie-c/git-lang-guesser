from collections import Counter


LANGUAGE_KEY = "language"


def count_languages(repos, filter_none=True):
    langs = (repo.get(LANGUAGE_KEY, None) for repo in repos)

    # filter out None
    if filter_none:
        langs = filter(lambda x: x is not None, langs)

    # a Counter does all the heavy lifting for us
    return Counter(langs)


def guess_favourite(repos):
    counter = count_languages(repos)

    if counter:
        [(favourite, count)] = counter.most_common(1)
        return favourite
    else:
        return None


if __name__ == "__main__":
    import pprint
    from . import git_requester

    my_repos = git_requester.get_public_repos_for_user("robbie-c")
    pprint.pprint(my_repos)

    lang = guess_favourite(my_repos)
    print(lang)