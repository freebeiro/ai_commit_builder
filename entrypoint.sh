#!/bin/sh

# Function to print messages if verbose mode is enabled
log() {
    if [ "$VERBOSE" = "true" ]; then
        echo "$1"
    fi
}

log "RUNNING ENTRYPOINT"

# Start Ollama service
log "Starting Ollama service..."
if [ "$VERBOSE" = "true" ]; then
    ollama serve &
else
    ollama serve > /dev/null 2>&1 &
fi
ollama_pid=$!

# Use wait-for-it.sh to wait until Ollama service is available
log "Waiting for Ollama service to be available..."
if [ "$VERBOSE" = "true" ]; then
    wait-for-it.sh localhost:11434 --timeout=60 --strict -- echo "Ollama service is up"
else
    wait-for-it.sh localhost:11434 --timeout=60 --strict -- echo "Ollama service is up" > /dev/null 2>&1
fi

# Pull the llama3 model if it doesn't exist
if ! ollama list | grep -q 'llama3:latest'; then
    log "Pulling llama3 model..."
    if [ "$VERBOSE" = "true" ]; then
        ollama pull llama3
    else
        ollama pull llama3 > /dev/null 2>&1
    fi
fi

# Check if Ollama service is running by querying it
retry=0
max_retries=5
while ! ollama list > /dev/null 2>&1 && [ $retry -lt $max_retries ]; do
    log "Waiting for Ollama service to be ready... (retry: $retry)"
    sleep 5
    retry=$((retry + 1))
done

if [ $retry -ge $max_retries ]; then
    log "Ollama service did not start. Exiting."
    exit 1
fi

log "Ollama service is ready."

# Run the generate_commit script
log "Running generate_commit..."
git config --global --add safe.directory /usr/src/project
generate_commit
