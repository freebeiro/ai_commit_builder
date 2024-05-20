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

def main():
    try:
        diff = get_git_diff()
        if not diff:
            print("No changes to commit.")
            return

        test_output, test_returncode = run_tests()
        if test_returncode != 0:
            print("Tests failed. Fix the issues before committing.")
            print(test_output)
            return

        if not check_coverage():
            print("Coverage is not 100%. Ensure all lines are covered before committing.")
            return

        extra_context = prompt("Provide any additional context for the commit message (optional): ")

        while True:
            commit_message = generate_commit_message(diff, extra_context)
            print("Generated commit message:")
            print(commit_message)
            action = input("Do you approve this commit message? (y/n) or type 'edit' to alter the prompt: ").lower()
            
            if action == 'y':
                create_commit(commit_message)
                print("Commit created successfully.")
                break
            elif action == 'n':
                print("Commit aborted.")
                return  # Exit the script
            elif action == 'edit':
                extra_context = prompt("Edit the context for the commit message (type 'cancel' to abort): ", default=extra_context)
                if extra_context.lower() == 'cancel':
                    print("Commit aborted.")
                    return  # Exit the script
            else:
                print("Invalid input. Please type 'y', 'n', or 'edit'.")
    except KeyboardInterrupt:
        print("\nCommit process interrupted. Exiting gracefully.")
        return