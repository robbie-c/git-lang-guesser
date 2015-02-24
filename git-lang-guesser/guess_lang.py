from collections import Counter


LANGUAGE_KEY = "language"


def count_languages(repos, filter_none=True):
    """
    Count the occurances of each language in a list of repositories

    :param repos: A list of repositories, which should be dictionaries with a "language" key
    :param filter_none: Whether to ignore repositories with no or None language
    :return: A collections.Counter representing the number of occurances
    """

    langs = (repo.get(LANGUAGE_KEY, None) for repo in repos)

    # filter out None
    if filter_none:
        langs = filter(lambda x: x is not None, langs)

    # a Counter does all the heavy lifting for us
    return Counter(langs)


def guess_favourite(repos):
    """
    Returns the most common language (except None) in the list of repos

    :param repos: A list of repositories, which should be dictionaries with a "language" key
    :return: The most common language. In the case of a tie, it is undefined which of the most common is chosen.
    """
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