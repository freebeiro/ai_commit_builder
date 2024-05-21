from prompt_toolkit import PromptSession
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
import subprocess
import requests

class GitCommitHelper:
    """
    Facilitates creation of Git commits with user input and automated checks.
    """

    def __init__(self):
        self.diff = None
        self.commit_message = None

    def get_git_diff(self):
        """Retrieves the current Git diff."""
        process = subprocess.run(['git', 'diff'], capture_output=True)
        self.diff = process.stdout.decode() if process.returncode == 0 else None

    def call_local_llama_model(self, prompt, extra_context=""):
        full_prompt = f"{prompt}\n\n{extra_context}"
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": full_prompt,
                "stream": False
            }
        )
        response_json = response.json()
        return response_json['response']

    def generate_commit_message(self, diff, extra_context=""):
        commit_template = """
    # Commit Title
    # (50 characters or less)

    # Detailed Description
    # (Wrap at 72 characters)
    #
    # - What changes were made?
    #
    # - Why were these changes made?
    #
    # - How do these changes address the problem?
    #
    # - Are there any side effects?
    #
    # Issue Reference
    # (Optional: Link to the issue or task this commit addresses)
    """
        prompt = f"Write a new commit message based on the following template and git diff:\n\n{commit_template}\n\nGit Diff:\n{diff}"
        return self.call_local_llama_model(prompt, extra_context)

    def create_commit(self, commit_message):
    def generate_commit_message(self):
        """Generates a commit message based on the diff and potentially more."""
        self.commit_message = f"Auto-generated commit message based on diff:\n{self.diff}"

    def create_commit(self):
        """Creates a Git commit with the generated message."""
        with open('.git/COMMIT_EDITMSG', 'w') as f:
            f.write(self.commit_message)
        subprocess.run(['git', 'commit', '-F', '.git/COMMIT_EDITMSG'])

    def prompt_for_confirmation(self):
        """Prompts the user for confirmation before creating a commit."""
        message = (
            "The following commit message has been generated:\n"
            f"{self.commit_message}\n"
            "Would you like to create the commit? (y/n): "
        )
        session = PromptSession()
        response = session.prompt(message, input=create_pipe_input(), output=DummyOutput())
        return response.lower() == 'y'
