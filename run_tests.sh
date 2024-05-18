#!/bin/bash

VERBOSE=0

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
        $1
    else
        $1 &>/dev/null
    fi
}

# Check for verbose option
if [ "$1" == "--verbose" ]; then
    VERBOSE=1
fi

# Check if .coveragerc exists and is properly formatted
COVERAGERC=".coveragerc"
check_file_exists $COVERAGERC

# Running tests with coverage
echo "Running tests with coverage..."
run_command "coverage run -m unittest discover"
if [ $? -ne 0 ]; then
    echo "Error: Failed to run tests with coverage. Ensure that test files are present and correctly configured."
    exit 1
fi

# Check if coverage data was collected
if ! coverage report --skip-covered &>/dev/null; then
    echo "No tests were run or no data was collected. Please ensure that your test files are present and properly configured."
    exit 1
fi

# Generating coverage report
echo "Generating coverage report..."
run_command "coverage report"
check_error "Failed to generate coverage report."

# Generating HTML coverage report
echo "Generating HTML coverage report..."
run_command "coverage html"
check_error "Failed to generate HTML coverage report."

# Checking if HTML report exists
HTML_REPORT="htmlcov/index.html"
check_file_exists $HTML_REPORT

# Opening HTML coverage report
echo "Opening HTML coverage report..."
run_command "open $HTML_REPORT"
check_error "Failed to open HTML coverage report."

echo "Tests and coverage reports generated successfully."
