import pytest
from tools.generate_commit.generate_commit import CommitGenerator
from unittest.mock import mock_open, patch
import subprocess

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
    
    # Mock the get_git_diff method
    mocker.patch.object(generator, 'get_git_diff')
    generator.diff = "diff --git a/file b/file\n"
    
    # Mock the prompt_toolkit prompt method
    mocker.patch('prompt_toolkit.prompt', return_value="")
    
    # Mock the generate_commit_message method
    mocker.patch.object(generator, 'generate_commit_message', return_value="Generated commit message")
    
    # Mock the builtins.input to simulate user input
    mocker.patch('builtins.input', side_effect=['y'])
    
    # Mock the create_commit method
    create_commit_mock = mocker.patch.object(generator, 'create_commit')
    
    # Run the main method
    generator.main()
    
    # Assert that create_commit was called once with the correct argument
    create_commit_mock.assert_called_once_with("Generated commit message")

def test_main_with_diff_edit_commit(mocker):
    generator = CommitGenerator()
    mocker.patch.object(generator, 'get_git_diff')
    generator.diff = "diff --git a/file b/file\n"
    mocker.patch('prompt_toolkit.prompt', return_value="")
    mocker.patch.object(generator, 'generate_commit_message', return_value="Generated commit message")
    mocker.patch('builtins.input', side_effect=['edit', 'y'])
    create_commit_mock = mocker.patch.object(generator, 'create_commit')

    generator.main()

    create_commit_mock.assert_called_once_with("Generated commit message")

def test_main_keyboard_interrupt(mocker):
    generator = CommitGenerator()
    mocker.patch.object(generator, 'get_git_diff', side_effect=KeyboardInterrupt)
    with pytest.raises(KeyboardInterrupt):
        generator.main()

def test_prompt_for_confirmation_no(mocker):
    generator = CommitGenerator()
    mocker.patch('prompt_toolkit.PromptSession.prompt', return_value='n')
    assert generator.prompt_for_confirmation() is False
