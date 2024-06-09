#!/usr/bin/env python3
import os
from commit_generator.git_handler import GitHandler
from commit_generator.message_editor import MessageEditor
from commit_generator.commit_generator import CommitGenerator

if __name__ == "__main__":
    repo_path = os.getcwd()
    git_handler = GitHandler(repo_path)
    message_editor = MessageEditor()
    model = "llama3:latest"  # Specify the desired model
    commit_generator = CommitGenerator(git_handler, message_editor, model)
    commit_generator.run()
