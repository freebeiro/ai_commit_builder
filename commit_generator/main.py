#!/usr/bin/env python3
import os
from git_handler import GitHandler
from message_editor import MessageEditor
from commit_generator import CommitGenerator

if __name__ == "__main__":
    repo_path = os.getcwd()
    git_handler = GitHandler(repo_path)
    message_editor = MessageEditor()
    model = "llama3:latest"
    commit_generator = CommitGenerator(git_handler, message_editor, model)
    commit_generator.run()
