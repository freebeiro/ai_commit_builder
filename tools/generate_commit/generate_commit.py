import requests
from prompt_toolkit import PromptSession
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
import subprocess
from prompt_toolkit import prompt

class CommitGenerator:
    def __init__(self):
        self.diff = None
        self.commit_message = None

    def get_git_diff(self):
        """Retrieves the current Git diff."""
        process = subprocess.run(['git', 'diff'], capture_output=True)
        self.diff = process.stdout.decode() if process.returncode == 0 else None

    def generate_commit_message(self, diff, extra_context=""):
        with open('commit_template.txt', 'r') as file:
            commit_template = file.read()
        
        prompt_text = f"Write a new commit message based on the following template and git diff:\n\n{commit_template}\n\nGit Diff:\n{diff}\n\n{extra_context}"
        return self.call_local_llama_model(prompt_text)

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

    def create_commit(self, commit_message):
        """Creates a Git commit with the generated message."""
        with open('.git/COMMIT_EDITMSG', 'w') as f:
            f.write(commit_message)
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
        try:
            self.get_git_diff()
            if not self.diff:
                print("No changes to commit.")
                return

            extra_context = prompt("Provide any additional context for the commit message (optional): ")

            while True:
                commit_message = self.generate_commit_message(self.diff, extra_context)
                print("Generated commit message:")
                print(commit_message)
                action = input("Do you approve this commit message? (y/n) or type 'edit' to alter the prompt: ").lower()

                if action == 'y':
                    self.create_commit(commit_message)
                    print("Commit created successfully.")
                    break
                elif action == 'n':
                    print("Commit aborted.")
                    break
                elif action == 'edit':
                    extra_context = prompt("Edit the context for the commit message: ", default=extra_context)
                else:
                    print("Invalid input. Please type 'y', 'n', or 'edit'.")
        except KeyboardInterrupt:
            print("\nCommit process interrupted. Exiting gracefully.")
            return

if __name__ == "__main__":
    generator = CommitGenerator()
    generator.main()

