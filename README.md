# AI Commit Builder

## Introduction

Welcome to AI Commit Builder! This tool helps you generate well-structured and detailed commit messages using the power of AI. By leveraging advanced language models, it ensures your commit messages are informative, consistent, and adhere to best practices. This tool is designed to work seamlessly with your existing Git workflow and can be easily integrated into any project.

## What It Does

AI Commit Builder automates the process of writing commit messages by analyzing your recent Git changes and using AI to generate a meaningful and detailed commit message. It supports the following features:
- Automatically generates commit messages based on the latest Git logs and diffs.
- Ensures commit messages follow a consistent format.
- Provides a prompt to add additional context or edit the generated message before committing.

## Technologies Used

- **Python 3.12**: For the core logic and interaction with Git.
- **Docker**: To create an isolated environment for the tool to run.
- **Docker Compose**: To manage multi-container Docker applications.
- **Ollama**: AI service used to generate commit messages.
- **wait-for-it**: Script to ensure dependent services are up and running before executing commands.

## Setup

### Prerequisites

- Git
- Docker
- Docker Compose

### Installation

1. **Clone the Repository**
    ```sh
    git clone <repository-url>
    cd ai_commit_builder
    ```

2. **Run the Setup Script**
    ```sh
    ./commit_generator/setup_generate_commit.sh
    ```

    This script performs the following actions:
    - Prompts for your Git username and email, and stores them in a `.env` file.
    - Creates a symbolic link for the `generate_commit_script.sh` script to make it accessible as `generate_commit`.
    - Sets up a virtual environment and installs necessary dependencies.

3. **Activate the Virtual Environment**
    ```sh
    source venv/bin/activate
    ```

## Usage

### Running in a New Git Repository

1. **Navigate to Your Project Directory**
    ```sh
    cd /path/to/your/project
    ```

2. **Run the `generate_commit` Command**
    ```sh
    generate_commit
    ```

    This command will:
    - Fetch the latest Git logs and Git diffs.
    - Will use a template format you provide or use the default template.
    - Use the AI model to generate a commit message based on the changes.
    - Provide a prompt to review and edit the generated message before committing.

### Example Workflow

1. **Make some changes in your repository**
    ```sh
    git add .
    ```

2. **Generate a Commit Message**
    ```sh
    generate_commit
    ```

3. **Review and Approve the Commit Message**
    - The tool will prompt you with a generated commit message.
    - You can approve (A), cancel (C), or edit (E) the message before committing.

## Troubleshooting

- **Configuration File Not Found**: If you encounter an error stating that the configuration file is not found, ensure that you have run the setup script from the root directory of the `ai_commit_builder` project.
- **Git Identity Issues**: If the commit fails due to missing Git identity, ensure that your `.env` file contains the correct Git username and email.

## Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

This README provides a comprehensive guide on setting up and using the AI Commit Builder tool. It covers all necessary steps to ensure users can integrate and use the tool effectively in their Git workflow.
