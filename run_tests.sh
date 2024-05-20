#!/bin/bash
export PYTHONPATH=$(pwd)

VERBOSE=0

# Function to log messages
log() {
    if [ $VERBOSE -eq 1 ]; then
        echo "$1"
    fi
}

# Function to check for errors
check_error() {
    if [ $? -ne 0 ]; then
        echo "Error: $1"
        exit 1
    fi
}

# Function to check if a file exists
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "File not found: $1"
        exit 1
    fi
}

# Function to run a command with optional verbosity
run_command() {
    if [ $VERBOSE -eq 1 ]; then
        eval $1
    else
        eval $1 &>/dev/null
    fi
}

# Check for verbose option
if [ "$1" == "--verbose" ]; then
    VERBOSE=1
fi

# Check if pytest.ini exists and is properly formatted
PYTESTINI="pytest.ini"
check_file_exists $PYTESTINI

# Running tests with pytest and coverage for the main app
log "Running tests with pytest and coverage for the main app..."
run_command "pytest --cov=app --cov-report=term-missing tests tools"
check_error "Failed to run tests with pytest and coverage for the main app. Ensure that test files are present and correctly configured."

# Generating HTML coverage report for the main app
log "Generating HTML coverage report for the main app..."
run_command "pytest --cov=app --cov-report=html tests tools"
check_error "Failed to generate HTML coverage report for the main app."

# Checking if HTML report exists for the main app
HTML_REPORT_APP="htmlcov/index.html"
check_file_exists $HTML_REPORT_APP

# Loop through tools and run tests
for tool in tools/*; do
    if [ -d "$tool" ]; then
        TOOL_NAME=$(basename "$tool")
        log "Running tests with pytest and coverage for the $TOOL_NAME tool..."
        run_command "pytest --cov=$tool --cov-report=term-missing"
        check_error "Failed to run tests with pytest and coverage for the $TOOL_NAME tool. Ensure that test files are present and correctly configured."

        log "Generating HTML coverage report for the $TOOL_NAME tool..."
        run_command "pytest --cov=$tool --cov-report=html"
        check_error "Failed to generate HTML coverage report for the $TOOL_NAME tool."

        HTML_REPORT_TOOL="htmlcov/index.html"
        check_file_exists $HTML_REPORT_TOOL

        log "HTML coverage report for the $TOOL_NAME tool generated at $HTML_REPORT_TOOL"
    fi
done

echo "Tests and coverage reports generated successfully."
