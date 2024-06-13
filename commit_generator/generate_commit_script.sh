#!/bin/bash

# Get the current directory dynamically
REPO_DIR=$(pwd)

# Fetch the git log and git diff from the current repository
GIT_LOG=$(git log -5 --pretty=format:"%h - %s (%ad)" --date=iso)
GIT_DIFF=$(git diff)

# Run the Docker command with the fetched values
docker compose run --rm -e GIT_LOG="$GIT_LOG" -e GIT_DIFF="$GIT_DIFF" generate_commit
