#!/usr/bin/env python3

import os
import sys
import subprocess

# Add the directory containing this script to the system path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from git_handler import GitHandler
from message_editor import MessageEditor
from commit_generator import CommitGenerator

def main():
    # Check if inside a git repository
    if not is_git_repo():
        print("This is not a git repository.")
        return

    repo_path = os.getcwd()
    script_path = os.path.dirname(os.path.realpath(__file__))
    project_template_path = os.path.join(repo_path, 'commit_template.txt')
    assistant_template_path = os.path.join(script_path, 'commit_template.txt')

    if os.path.isfile(project_template_path):
        template_path = project_template_path
        print(f"Using project template path: {template_path}")
    elif os.path.isfile(assistant_template_path):
        template_path = assistant_template_path
        print(f"Using assistant template path: {template_path}")
    else:
        print("No commit template found.")
        return

    prompt_path = os.path.join(script_path, 'llm_prompt.txt')
    print(f"Prompt path: {prompt_path}")

    git_log = os.getenv('GIT_LOG')
    git_diff = os.getenv('GIT_DIFF')

    git_handler = GitHandler(repo_path)
    message_editor = MessageEditor()

    generator = CommitGenerator(git_handler, message_editor, git_log=git_log, git_diff=git_diff)
    generator.run(template_path=template_path, prompt_path=prompt_path)

def is_git_repo():
    try:
        subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

if __name__ == "__main__":
    main()
