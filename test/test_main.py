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
