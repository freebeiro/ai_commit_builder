from prompt_toolkit import PromptSession
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
import subprocess

class GitCommitHelper:
    """
    Facilitates creation of Git commits with user input and automated checks.
    """

    def __init__(self):
        self.diff = None
        self.commit_message = None
        self.generate_commit_message()

    def get_git_diff(self):
        """Retrieves the current Git diff."""
        process = subprocess.run(['git', 'diff'], capture_output=True)
        self.diff = process.stdout.decode() if process.returncode == 0 else None

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
