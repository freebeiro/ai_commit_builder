#!/bin/bash

# Load the configuration
CONFIG_FILE="$HOME/.generate_commit_config"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Configuration file not found. Please run the setup script first."
    exit 1
fi

# Source the configuration file to get the path
source "$CONFIG_FILE"

# Check if the COMMIT_GENERATOR_DIR is set
if [ -z "$COMMIT_GENERATOR_DIR" ]; then
    echo "Commit generator directory is not set in the configuration file."
    exit 1
fi

# Get the current directory dynamically
REPO_DIR=$(pwd)

# Check if inside a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "This is not a git repository."
    exit 1
fi

# Fetch the git log and git diff from the current repository
GIT_LOG=$(git log -5 --pretty=format:"%h - %s (%ad)" --date=iso)
GIT_DIFF=$(git diff)

# Export the environment variables
export GIT_LOG
export GIT_DIFF

# Check for verbose flag
VERBOSE_FLAG="false"
if [ "$1" = "-verbose" ]; then
    VERBOSE_FLAG="true"
fi

# Run the Docker command with the fetched values
docker compose -f "$COMMIT_GENERATOR_DIR/docker-compose.yml" run --rm -e GIT_LOG="$GIT_LOG" -e GIT_DIFF="$GIT_DIFF" -e VERBOSE="$VERBOSE_FLAG" generate_commit
