import pytest
parametrize = pytest.mark.parametrize

from git_lang_guesser import guess_lang

LANGUAGE = "language"


example_data = [
    {LANGUAGE: "HTML"},
    {LANGUAGE: "Java"},
    {LANGUAGE: "Python"},
    {LANGUAGE: "Python"},
    {LANGUAGE: "C"},
]
expected_count = {
    "HTML": 1,
    "Java": 1,
    "Python": 2,
    "C": 1,
}
expected_favourite = "Python"


class TestCountLanguages(object):
    def test_basic(self):
        """Ensure basic usage does the right thing"""
        counter = guess_lang.count_languages(example_data)
        assert(dict(counter) == expected_count)

    def test_empty(self):
        """Ensure we can an empty repository list"""
        counter = guess_lang.count_languages([])
        assert(dict(counter) == {})

    @parametrize('filter_none, expected', [(True, {}), (False, {None: 1})])
    def test_none(self, filter_none, expected):
        """Test that filter_none works"""
        counter = guess_lang.count_languages([{LANGUAGE: None}], filter_none=filter_none)
        assert(dict(counter) == expected)

    def test_language_missing(self):
        """Ensure we can handle a repository with language missing"""
        counter = guess_lang.count_languages([{LANGUAGE: "Python"}, {}])
        assert(dict(counter) == {"Python": 1})


class TestGuessFavourite(object):
    def test_basic(self):
        """Ensure basic usage does the right thing"""
        favourite = guess_lang.guess_favourite(example_data)
        assert(favourite == expected_favourite)

    def test_empty(self):
        """Ensure we can an empty repository list"""
        favourite = guess_lang.guess_favourite([])
        assert(favourite is None)