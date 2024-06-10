#!/usr/bin/env python3

import os
import sys
import subprocess

# Add the parent directory of the script to the system path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(script_dir))

from git_handler import GitHandler
from message_editor import MessageEditor
from commit_tool import CommitGenerator  # Updated import

def main():
    # Check if inside a git repository``
    if not is_git_repo():
        print("This is not a git repository.")
        return

    repo_path = os.getcwd()
    project_template_path = os.path.join(repo_path, 'commit_template.txt')
    assistant_template_path = os.path.join(script_dir, 'commit_template.txt')

    if os.path.isfile(project_template_path):
        template_path = project_template_path
    elif os.path.isfile(assistant_template_path):
        template_path = assistant_template_path
    else:
        print("No commit template found.")
        return

    prompt_path = os.path.join(script_dir, 'llm_prompt.txt')

    git_handler = GitHandler(repo_path)
    message_editor = MessageEditor()

    generator = CommitGenerator(git_handler, message_editor)
    generator.run(template_path=template_path, prompt_path=prompt_path)

def is_git_repo():
    try:
        subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

if __name__ == "__main__":
    main()
