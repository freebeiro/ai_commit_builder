import pytest
from tools.generate_commit.generate_commit import CommitGenerator
from unittest.mock import mock_open, patch, Mock
import subprocess
import runpy



def test_get_git_diff(mocker):
    generator = CommitGenerator()
    mocker.patch('subprocess.run', return_value=mocker.Mock(stdout=b"diff --git a/file b/file\n", returncode=0))
    generator.get_git_diff()
    assert generator.diff == "diff --git a/file b/file\n"

def test_generate_commit_message(mocker):
    generator = CommitGenerator()
    generator.diff = "diff --git a/file b/file\n"
    mocker.patch('builtins.open', mock_open(read_data="Commit template content"))
    mocker.patch.object(generator, 'call_local_llama_model', return_value="Generated commit message")
    commit_message = generator.generate_commit_message(generator.diff)
    assert commit_message == "Generated commit message"

def test_call_local_llama_model(mocker):
    generator = CommitGenerator()
    mock_response = mocker.Mock()
    mock_response.json.return_value = {'response': 'Generated commit message'}
    mocker.patch('requests.post', return_value=mock_response)
    response = generator.call_local_llama_model("prompt")
    assert response == "Generated commit message"

def test_create_commit(mocker):
    generator = CommitGenerator()
    generator.commit_message = "Test commit message"
    mocker.patch('builtins.open', mock_open())
    mocker.patch('subprocess.run')
    generator.create_commit(generator.commit_message)
    open.assert_called_once_with('.git/COMMIT_EDITMSG', 'w')
    open().write.assert_called_once_with("Test commit message")
    subprocess.run.assert_called_once_with(['git', 'commit', '-F', '.git/COMMIT_EDITMSG'])

def test_prompt_for_confirmation(mocker):
    generator = CommitGenerator()
    mocker.patch('prompt_toolkit.PromptSession.prompt', return_value='y')
    assert generator.prompt_for_confirmation() is True

def test_main_no_diff(mocker):
    generator = CommitGenerator()
    mocker.patch.object(generator, 'get_git_diff', return_value=None)
    mocker.patch('prompt_toolkit.prompt', return_value="")
    generator.main()
    assert generator.diff is None

def test_main_with_diff_approve_commit(mocker):
    generator = CommitGenerator()
    mocker.patch.object(generator, 'get_git_diff')
    generator.diff = "diff --git a/file b/file\n"
    mocker.patch('prompt_toolkit.prompt', return_value="")
    mocker.patch.object(generator, 'generate_commit_message', return_value="Generated commit message")
    mock_input = mocker.patch('builtins.input', side_effect=['y'])
    mock_prompt_session = mocker.patch('prompt_toolkit.PromptSession.prompt', return_value='y')
    create_commit_mock = mocker.patch.object(generator, 'create_commit')
    print("Running generator.main()")
    generator.main()
    print("Finished generator.main()")
    create_commit_mock.assert_called_once_with("Generated commit message")
    mock_input.assert_called_with("Do you approve this commit message? (y/n) or type 'edit' to alter the prompt: ")
    mock_prompt_session.assert_called_once()


def test_main_with_diff_abort_commit(mocker):
    generator = CommitGenerator()
    mocker.patch.object(generator, 'get_git_diff')
    generator.diff = "diff --git a/file b/file\n"
    mocker.patch('prompt_toolkit.prompt', return_value="")
    mocker.patch.object(generator, 'generate_commit_message', return_value="Generated commit message")
    mocker.patch('builtins.input', side_effect=['n'])
    mocker.patch('prompt_toolkit.PromptSession.prompt', return_value='n')
    create_commit_mock = mocker.patch.object(generator, 'create_commit')
    generator.main()
    assert create_commit_mock.call_count == 0


def test_main_with_diff_edit_commit(mocker):
    generator = CommitGenerator()
    mocker.patch.object(generator, 'get_git_diff')
    generator.diff = "diff --git a/file b/file\n"
    mocker.patch('prompt_toolkit.prompt', return_value="")
    mocker.patch.object(generator, 'generate_commit_message', return_value="Generated commit message")
    mocker.patch('builtins.input', side_effect=['edit', 'y'])
    mocker.patch('prompt_toolkit.PromptSession.prompt', side_effect=lambda message, **kwargs: "")
    create_commit_mock = mocker.patch.object(generator, 'create_commit')
    generator.main()
    create_commit_mock.assert_called_once_with("Generated commit message")

def test_main_keyboard_interrupt(mocker):
    generator = CommitGenerator()
    mocker.patch.object(generator, 'get_git_diff', side_effect=KeyboardInterrupt)
    print_mock = mocker.patch('builtins.print')
    generator.main()
    print_mock.assert_any_call("\nCommit process interrupted. Exiting gracefully.")

def test_prompt_for_confirmation_no(mocker):
    generator = CommitGenerator()
    mocker.patch('prompt_toolkit.PromptSession.prompt', return_value='n')
    assert generator.prompt_for_confirmation() is False

def test_main_with_diff_invalid_input(mocker):
    generator = CommitGenerator()
    mocker.patch.object(generator, 'get_git_diff')
    generator.diff = "diff --git a/file b/file\n"
    mocker.patch('prompt_toolkit.prompt', return_value="")
    mocker.patch.object(generator, 'generate_commit_message', return_value="Generated commit message")
    mocker.patch('builtins.input', side_effect=['invalid', 'y'])
    create_commit_mock = mocker.patch.object(generator, 'create_commit')
    mocker.patch('prompt_toolkit.PromptSession.prompt', return_value='')
    generator.main()
    create_commit_mock.assert_called_once_with("Generated commit message")

def test_main_execution(mocker):
    import tools.generate_commit.generate_commit as gc
    mocker.patch.object(gc, 'CommitGenerator', autospec=True)
    generator_instance = gc.CommitGenerator.return_value
    generator_instance.main = Mock()
    mocker.patch('prompt_toolkit.prompt', return_value="")
    mocker.patch('builtins.input', return_value='y')
    runpy.run_module("tools.generate_commit.generate_commit", run_name="__main__")

