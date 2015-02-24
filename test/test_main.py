import http.client

import pytest
import requests

from git_lang_guesser import exceptions
from git_lang_guesser import main
from git_lang_guesser import git_requester


LANGUAGE = "language"

test_username = "TestUser"
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


class DummyResponse(requests.Response):
    def __init__(self, status_code, text):
        super(DummyResponse, self).__init__()
        self.status_code = status_code
        self.__text = text

    @property
    def text(self):
        return self.__text


class TestDoGuess(object):

    def test_basic(self, monkeypatch, capsys):
        """Test that basic usage works"""

        def mock_request(username):
            assert(username == test_username)
            return example_data
        monkeypatch.setattr(git_requester, "get_public_repos_for_user", mock_request)

        main.do_guess(username=test_username, list_all=False)

        out, err = capsys.readouterr()

        assert(out.strip() == expected_favourite)

    def test_user_not_found(self, monkeypatch, capsys):
        def mock_request(username):
            assert(username == test_username)
            raise exceptions.RequestFailed(DummyResponse(http.client.NOT_FOUND, ""))
        monkeypatch.setattr(git_requester, "get_public_repos_for_user", mock_request)

        with pytest.raises(SystemExit):
            main.do_guess(username=test_username, list_all=False)

        out, err = capsys.readouterr()

        assert(out.strip() == "User TestUser not found")

    def test_unknown_error(self, monkeypatch, capsys):
        def mock_request(username):
            assert(username == test_username)
            raise exceptions.RequestFailed(DummyResponse(418, "Teapot"))
        monkeypatch.setattr(git_requester, "get_public_repos_for_user", mock_request)

        with pytest.raises(SystemExit):
            main.do_guess(username=test_username, list_all=False)

        out, err = capsys.readouterr()

        assert(out.strip() == "HTTP error code 418: Teapot")

    def test_no_repos(self, monkeypatch, capsys):
        def mock_request(username):
            assert(username == test_username)
            return []
        monkeypatch.setattr(git_requester, "get_public_repos_for_user", mock_request)

        with pytest.raises(SystemExit):
            main.do_guess(username=test_username, list_all=False)

        out, err = capsys.readouterr()

        assert(out.strip() == "User does not have any public repos")
