#!/bin/bash

# Define the directory containing generate_commit.py
COMMIT_GENERATOR_DIR="commit_generator"

# Ensure the script is run from the root directory of the project
if [ ! -d "$COMMIT_GENERATOR_DIR" ]; then
    echo "Error: This script must be run from the root directory of the commit_builder project."
    exit 1
fi

# Function to print status messages
print_status() {
    if [ $? -eq 0 ]; then
        echo "$1: OK"
    else
        echo "$1: FAILED"
        exit 1
    fi
}

# Prompt the user for Git username and email
echo "Please enter your Git username (this is necessary for committing changes):"
read GIT_USER_NAME

echo "Please enter your Git email (this is necessary for committing changes):"
read GIT_USER_EMAIL

# Create a .env file with the provided username and email
echo -e "GIT_USER_NAME=${GIT_USER_NAME}\nGIT_USER_EMAIL=${GIT_USER_EMAIL}" > .env
print_status "Creating .env file with Git configuration"

# Store the path to ai_commit_builder in a config file
CONFIG_FILE="$HOME/.generate_commit_config"
echo "COMMIT_GENERATOR_DIR=$(pwd)" > "$CONFIG_FILE"
print_status "Storing configuration"

# Create a symbolic link
echo "Creating symbolic link for generate_commit_script.sh..."
sudo ln -sf $(pwd)/$COMMIT_GENERATOR_DIR/generate_commit_script.sh /usr/local/bin/generate_commit
print_status "Creating symbolic link"

# Check if the symlink was created successfully
if [ -L /usr/local/bin/generate_commit ]; then
    echo "Symbolic link created: OK"
else
    echo "Symbolic link creation failed: FAILED"
    exit 1
fi

# Make the symbolic link executable
echo "Making symbolic link executable..."
sudo chmod +x /usr/local/bin/generate_commit
print_status "Making symbolic link executable"

# Check if virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    print_status "Creating virtual environment"
else
    echo "Virtual environment already exists: OK"
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
print_status "Activating virtual environment"

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt
print_status "Installing required packages"

echo "Setup complete. Virtual environment is ready and dependencies are installed."

# Optional: Notify the user how to run the script
echo "To run the generate_commit script, use:"
echo "generate_commit"
