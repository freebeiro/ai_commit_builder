from prompt_toolkit import PromptSession
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput

class GitCommitHelper:
    """
    Facilitates creation of Git commits with user input and automated checks.
    """

    def __init__(self):
        self.diff = None
        self.test_output = None
        self.test_returncode = None
        self.coverage_passed = None
        self.commit_message = None

    def get_git_diff(self):
        """Retrieves the current Git diff."""
        process = subprocess.run(['git', 'diff'], capture_output=True)
        self.diff = process.stdout.decode() if process.returncode == 0 else None

    def run_tests(self):
        """Runs unit tests and captures output and return code."""
        process = subprocess.run(['pytest'], capture_output=True)
        self.test_output = process.stdout.decode()
        self.test_returncode = process.returncode

    def check_coverage(self):
        """Checks code coverage (implementation based on your coverage tool)."""
        # Replace this with your specific coverage check logic
        self.coverage_passed = True  # Placeholder

    def generate_commit_message(self):
        """Generates a commit message based on the diff and potentially more."""
        # You can integrate a service like Llama here for advanced message generation
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

    def main(self):
        """Main execution flow for the class."""
        self.get_git_diff()
        if not self.diff:
            print("No changes detected. Skipping commit creation.")
            return

        self.run_tests()
        self.check_coverage()

        if self.test_returncode != 0 or not self.coverage_passed:
            print("Tests failed or coverage did not meet requirements.")
            return

        self.generate_commit_message()

        if self.prompt_for_confirmation():
            self.create_commit()
            print("Commit created successfully.")
