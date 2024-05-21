import pytest
from tools.generate_commit.generate_commit import GitCommitHelper
from unittest.mock import mock_open, patch
import subprocess

def test_get_git_diff(mocker):
    helper = GitCommitHelper()
    mocker.patch('subprocess.run', return_value=mocker.Mock(stdout=b"diff --git a/file b/file\n", returncode=0))
    helper.get_git_diff()
    assert helper.diff == "diff --git a/file b/file\n"

def test_generate_commit_message():
    helper = GitCommitHelper()
    helper.diff = "diff --git a/file b/file\n"
    helper.generate_commit_message()
    assert helper.commit_message == "Auto-generated commit message based on diff:\n" + helper.diff

def test_create_commit(mocker):
    helper = GitCommitHelper()
    helper.commit_message = "Test commit message"
    mocker.patch('builtins.open', mock_open())
    mocker.patch('subprocess.run')
    helper.create_commit()
    open.assert_called_once_with('.git/COMMIT_EDITMSG', 'w')
    open().write.assert_called_once_with("Test commit message")
    subprocess.run.assert_called_once_with(['git', 'commit', '-F', '.git/COMMIT_EDITMSG'])

def test_prompt_for_confirmation_yes(mocker):
    helper = GitCommitHelper()
    mocker.patch('prompt_toolkit.PromptSession.prompt', return_value='y')
    assert helper.prompt_for_confirmation() is True

def test_prompt_for_confirmation_no(mocker):
    helper = GitCommitHelper()
    mocker.patch('prompt_toolkit.PromptSession.prompt', return_value='n')
    assert helper.prompt_for_confirmation() is False

@pytest.mark.parametrize("input_side_effect, expected", [
    (['y'], True),
    (['n'], False),
    (KeyboardInterrupt, False)
])
def test_prompt_for_confirmation_param(mocker, input_side_effect, expected):
    helper = GitCommitHelper()
    mocker.patch('prompt_toolkit.PromptSession.prompt', side_effect=input_side_effect)
    assert helper.prompt_for_confirmation() == expected

def test_main_no_diff(mocker):
    helper = GitCommitHelper()
    mocker.patch.object(helper, 'get_git_diff', return_value=None)
    generate_commit_message_mock = mocker.patch.object(helper, 'generate_commit_message')
    prompt_for_confirmation_mock = mocker.patch.object(helper, 'prompt_for_confirmation')
    create_commit_mock = mocker.patch.object(helper, 'create_commit')


    generate_commit_message_mock.assert_not_called()
    prompt_for_confirmation_mock.assert_not_called()
    create_commit_mock.assert_not_called()

def test_main_with_changes_tests_fail(mocker):
    helper = GitCommitHelper()
    mocker.patch.object(helper, 'get_git_diff', return_value="diff --git a/file b/file\n")
    generate_commit_message_mock = mocker.patch.object(helper, 'generate_commit_message')
    prompt_for_confirmation_mock = mocker.patch.object(helper, 'prompt_for_confirmation')
    create_commit_mock = mocker.patch.object(helper, 'create_commit')
    generate_commit_message_mock.assert_not_called()
    prompt_for_confirmation_mock.assert_not_called()
    create_commit_mock.assert_not_called()

def test_main_with_changes_coverage_fail(mocker):
    helper = GitCommitHelper()
    mocker.patch.object(helper, 'get_git_diff', return_value="diff --git a/file b/file\n")
    generate_commit_message_mock = mocker.patch.object(helper, 'generate_commit_message')
    prompt_for_confirmation_mock = mocker.patch.object(helper, 'prompt_for_confirmation')
    create_commit_mock = mocker.patch.object(helper, 'create_commit')
    generate_commit_message_mock.assert_not_called()
    prompt_for_confirmation_mock.assert_not_called()
    create_commit_mock.assert_not_called()

def test_main_with_changes_commit_declined(mocker):
    helper = GitCommitHelper()
    mocker.patch.object(helper, 'get_git_diff', return_value="diff --git a/file b/file\n")
    generate_commit_message_mock = mocker.patch.object(helper, 'generate_commit_message')
    prompt_for_confirmation_mock = mocker.patch.object(helper, 'prompt_for_confirmation', return_value=False)
    create_commit_mock = mocker.patch.object(helper, 'create_commit')

    helper.main()

    generate_commit_message_mock.assert_called_once()
    prompt_for_confirmation_mock.assert_called_once()
    create_commit_mock.assert_not_called()

def test_main_with_changes_success(mocker):
    helper = GitCommitHelper()
    mocker.patch.object(helper, 'get_git_diff', return_value="diff --git a/file b/file\n")
    generate_commit_message_mock = mocker.patch.object(helper, 'generate_commit_message')
    prompt_for_confirmation_mock = mocker.patch.object(helper, 'prompt_for_confirmation', return_value=True)
    create_commit_mock = mocker.patch.object(helper, 'create_commit')
    generate_commit_message_mock.assert_called_once()
    prompt_for_confirmation_mock.assert_called_once()
    create_commit_mock.assert_called_once()
