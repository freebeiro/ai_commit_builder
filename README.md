
# AI Commit Builder

AI Commit Builder is a tool designed to help you generate meaningful commit messages for your git repositories using AI. It uses Ollama for natural language processing and helps create standardized, informative commit messages based on your git logs and diffs.

## Features

- Generates commit messages based on git log and diff
- Uses AI to create meaningful commit messages
- Easy setup and usage

## Technologies Used

- Python
- Docker
- Ollama
- Git

## Setup

1. **Clone the Repository**

    ```sh
    git clone https://github.com/yourusername/ai_commit_builder.git
    cd ai_commit_builder
    ```

2. **Run the Setup Script**

    ```sh
    ./commit_generator/setup_generate_commit.sh
    ```

3. **Configure Git (if not already done)**

    During the setup process, you will be prompted to enter your Git username and email. These will be stored in a `.env` file.

4. **Activate the Virtual Environment**

    ```sh
    source venv/bin/activate
    ```

5. **Generate Commit Messages**

    Navigate to any git repository and run:

    ```sh
    generate_commit
    ```

## Verbose Mode

If you want to see detailed logs while generating the commit message, you can run the `generate_commit` command with the `--verbose` flag:

```sh
generate_commit --verbose
```

## Running Tests

To run the tests for AI Commit Builder, ensure you have `pytest` installed:

```sh
pip install -r requirements.txt
```

Then, you can run the tests using the following command:

```sh
pytest
```

This will execute all the tests in the `tests` directory and provide you with a report of the results.

