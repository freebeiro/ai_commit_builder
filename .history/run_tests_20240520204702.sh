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

# Start coverage measurement early
COV_CMD="coverage run -m pytest --cov=app --cov=tools --cov=tests --cov-report=term-missing tests tools"
log "Running tests with coverage..."
run_command "$COV_CMD"
check_error "Failed to run tests with coverage."

# Generating HTML coverage report
log "Generating HTML coverage report..."
run_command "coverage html"
check_error "Failed to generate HTML coverage report."

# Checking if HTML report exists
HTML_REPORT="htmlcov/index.html"
check_file_exists $HTML_REPORT

echo "Tests and coverage reports generated successfully."
echo "Tests and coverage reports generated successfully."