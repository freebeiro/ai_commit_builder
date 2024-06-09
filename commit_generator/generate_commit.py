#!/usr/bin/env python3
import os
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

class CommitGenerator:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def _get_git_log(self, num_commits=5):
        try:
            result = subprocess.run(
                ["git", "log", f"-{num_commits}"],
                cwd=self.repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            result.check_returncode()
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting git log: {e.stderr}")
            return None

    def _get_git_diff(self):
        try:
            result = subprocess.run(
                ["git", "diff"],
                cwd=self.repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            result.check_returncode()
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting git diff: {e.stderr}")
            return None

    def _generate_commit_message(self, log, diff, template_path, extra_message):
        commit_message = f"Commit Message\nLog:\n{log}\nDiff:\n{diff}\nExtra Message:\n{extra_message}"
        return commit_message

    def _capture_multiline_input(self, prompt_text, initial_message=""):
        session = PromptSession()
        bindings = KeyBindings()

        @bindings.add('c-d')
        def _(event):
            event.app.exit(result=event.app.current_buffer.document.text)

        return session.prompt(prompt_text, multiline=True, key_bindings=bindings, default=initial_message)

    def _capture_user_input(self):
        extra_message = self._capture_multiline_input("Enter an extra message for the commit (Press Ctrl-D to finish):\n")
        return extra_message

    def _preview_commit_message(self, commit_message):
        print("\nPreview of generated commit message:\n")
        print(commit_message)

    def _handle_user_response(self, log, diff, template_path, extra_message, commit_message):
        while True:
            self._preview_commit_message(commit_message)
            response = input("\nDo you approve, cancel, or want to edit the message? (A/C/E): ")
            if response.upper() == "A":
                print("Committing with the generated message...")
                # Call `git commit` with the generated message
                # subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path)
                break
            elif response.upper() == "C":
                print("Canceling the commit...")
                break
            elif response.upper() == "E":
                extra_message = self._capture_multiline_input("Edit the extra message (Press Ctrl-D to finish):\n", extra_message)
                commit_message = self._generate_commit_message(log, diff, template_path, extra_message)
            else:
                print("Invalid response. Please try again.")

    def run(self, template_path="commit_template.txt"):
        log = self._get_git_log()
        diff = self._get_git_diff()
        extra_message = self._capture_user_input()
        commit_message = self._generate_commit_message(log, diff, template_path, extra_message)
        self._handle_user_response(log, diff, template_path, extra_message, commit_message)

if __name__ == "__main__":
    repo_path = os.getcwd()
    generator = CommitGenerator(repo_path)
    generator.run()
