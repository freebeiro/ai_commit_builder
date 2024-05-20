import sys
import os
import pytest
from unittest.mock import patch, mock_open
from tools.generate_commit.generate_commit import GitCommitHelper
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput
from prompt_toolkit.shortcuts import PromptSession

# Temporarily add the parent directory to PYTHONPATH within a fixture
@pytest.fixture(autouse=True)
def add_parent_to_pythonpath():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    yield
    sys.path.pop(0)

# Mock subprocess.run
@pytest.fixture
def mock_subprocess_run(mocker):
    return mocker.patch('subprocess.run')

def test_get_git_diff(mock_subprocess_run):
    helper = GitCommitHelper()
    mock_subprocess_run.return_value.stdout = b"diff --git a/file b/file\n"
    helper.get_git_diff()
    assert helper.diff == "diff --git a/file b/file\n"

def test_run_tests(mock_subprocess_run):
    helper = GitCommitHelper()
    mock_subprocess_run.return_value.stdout = b"test output"
    mock_subprocess_run.return_value.returncode = 0
    helper.run_tests()
    assert helper.test_output == "test output"
    assert helper.test_returncode == 0

def test_check_coverage(mock_subprocess_run, mocker):
    mock_subprocess_run.return_value.stdout = b"coverage output"
    mock_open_func = mocker.patch("builtins.open", mock_open(read_data="100%"))
    assert check_coverage() is True
    mock_open_func.assert_called_with('htmlcov/index.html')

def test_generate_commit_message(mocker):
    mocker.patch('tools.generate_commit.generate_commit.call_local_llama_model', return_value="Generated commit message based on diff")
    diff = "diff --git a/file b/file\n"
    message = generate_commit_message(diff)
    assert message == "Generated commit message based on diff"

def test_create_commit(mocker):
    mock_open_func = mocker.patch("builtins.open", mock_open())
    mock_subprocess_run = mocker.patch('subprocess.run')
    create_commit("Commit message")
    mock_open_func.assert_called_with('.git/COMMIT_EDITMSG', 'w')
    mock_subprocess_run.assert_called_with(['git', 'commit', '-F', '.git/COMMIT_EDITMSG'])

def test_main_no_changes(mocker):
    mocker.patch('tools.generate_commit.generate_commit.get_git_diff', return_value="")
    main()
    assert True  # Just to ensure it runs without error

@pytest.mark.parametrize("input_side_effect, prompt_return_value", [
    (['y'], ''),
    (['n'], ''),
    (['edit', 'cancel'], ''),
    (KeyboardInterrupt, None)
])
def test_main(mocker, input_side_effect, prompt_return_value):
    mocker.patch('tools.generate_commit.generate_commit.get_git_diff', return_value="diff --git a/file b/file\n")
    mocker.patch('tools.generate_commit.generate_commit.run_tests', return_value=("test output", 0))
    mocker.patch('tools.generate_commit.generate_commit.check_coverage', return_value=True)
    mocker.patch('tools.generate_commit.generate_commit.generate_commit_message', return_value="Generated commit message")
    mocker.patch('tools.generate_commit.generate_commit.create_commit')
    mocker.patch('builtins.input', side_effect=input_side_effect)
    with create_pipe_input() as inp:
        session = PromptSession(input=inp, output=DummyOutput())
        mocker.patch('prompt_toolkit.prompt', side_effect=lambda *args, **kwargs: session.prompt())
        main()
    assert True  # Ensure it runs without error

