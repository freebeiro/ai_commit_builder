import os
import ollama
import subprocess

class CommitGenerator:
    def __init__(self, git_handler, message_editor, model="llama3:latest"):
        self.git_handler = git_handler
        self.message_editor = message_editor
        self.model = model

    def _generate_commit_message(self, change_summary, template_path, extra_message, prompt_path):
        with open(template_path, "r") as f:
            template = f.read()

        with open(prompt_path, "r") as f:
            llm_prompt = f.read()

        # Fill in the placeholders in the LLM prompt
        prompt = llm_prompt.format(template=template, change_summary=change_summary, extra_message=extra_message)

        # Call ollama.generate with the filled prompt
        generated_response = ollama.generate(model=self.model, prompt=prompt)

        # Extract the message from the response
        generated_message = generated_response['response'].strip()

        # Split the response using the beginning of the template to find the main content
        start_template = template.split("\n")[0]  # Get the first line of the template
        if start_template in generated_message:
            generated_message = generated_message.split(start_template, 1)[-1].strip()
        
        return generated_message

    def _preview_commit_message(self, commit_message):
        print("\nPreview of generated commit message:\n")
        print(commit_message)

    def _handle_user_response(self, change_summary, template_path, extra_message, commit_message, prompt_path):
        while True:
            self._preview_commit_message(commit_message)
            try:
                response = input("\nDo you approve, cancel, or want to edit the message? (A/C/E): ")
            except EOFError:
                print("\nInput interrupted. Cancelling the commit...")
                break
            except KeyboardInterrupt:
                print("\nCommit cancelled.")
                break

            if response.upper() == "A":
                print("Committing with the generated message...")
                self._commit_with_message(commit_message)
                break
            elif response.upper() == "C":
                print("Canceling the commit...")
                break
            elif response.upper() == "E":
                extra_message = self.message_editor.capture_multiline_input("Edit the extra message (Press Ctrl-D to finish):\n", extra_message)
                commit_message = self._generate_commit_message(change_summary, template_path, extra_message, prompt_path)
            else:
                print("Invalid response. Please try again.")

    def _commit_with_message(self, commit_message):
        try:
            result = subprocess.run(["git", "commit", "-m", commit_message], cwd=self.git_handler.repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            result.check_returncode()
            print("Commit successful!")
        except subprocess.CalledProcessError as e:
            print(f"Error during commit: {e.stderr}")

    def run(self, template_path=None, prompt_path=None):
        if template_path is None:
            template_path = os.path.join(os.path.dirname(__file__), 'commit_template.txt')
        if prompt_path is None:
            prompt_path = os.path.join(os.path.dirname(__file__), 'llm_prompt.txt')

        if not self.git_handler.has_staged_changes():
            print("No changes staged for commit.")
            return

        change_summary = self.git_handler.get_change_summary()
        try:
            extra_message = self.message_editor.capture_multiline_input("Enter an extra message for the commit (Press Ctrl-D to finish):\n")
        except EOFError:
            print("\nInput interrupted. Cancelling the commit...")
            return
        except KeyboardInterrupt:
            print("\nCommit cancelled.")
            return

        commit_message = self._generate_commit_message(change_summary, template_path, extra_message, prompt_path)
        self._handle_user_response(change_summary, template_path, extra_message, commit_message, prompt_path)
