#!/bin/bash

set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Get the branch name from the argument or default to main
BRANCH=${1:-main}

# Install Docker if not installed
if ! command_exists docker; then
    echo "Docker is not installed. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
else
    echo "Docker is already installed."
fi

# Install Docker Compose if not installed
if ! command_exists docker-compose; then
    echo "Docker Compose is not installed. Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '(?<=tag_name\": \"v)[^"]*')/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "Docker Compose is already installed."
fi

# Clone the ai_commit_builder repository
if [ ! -d "ai_commit_builder" ]; then
    echo "Cloning the ai_commit_builder repository..."
    git clone -b "$BRANCH" https://github.com/freebeiro/ai_commit_builder.git
else
    echo "ai_commit_builder repository already exists."
fi

cd ai_commit_builder

# Build the Docker image
echo "Building the Docker image..."
docker-compose build

# Create the generate_commit script
echo "Creating the generate_commit script..."
sudo tee /usr/local/bin/generate_commit > /dev/null <<EOL
#!/bin/bash
cd /usr/src/app/commit_generator
docker-compose --project-directory \${PWD} run --rm generate_commit
EOL

# Make the script executable
sudo chmod +x /usr/local/bin/generate_commit

echo "Setup complete. You can now use the 'generate_commit' command to generate commit messages."
