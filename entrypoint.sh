#!/bin/sh
echo "RUNNING ENTRYPOINT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
# Start Ollama service
echo "Starting Ollama service..."
ollama serve &
ollama_pid=$!

# Use wait-for-it.sh to wait until Ollama service is available
wait-for-it.sh localhost:11434 --timeout=60 --strict -- echo "Ollama service is up"

# Pull the llama3 model if it doesn't exist
if ! ollama list | grep -q 'llama3:latest'; then
    echo "Pulling llama3 model..."
    ollama pull llama3
fi

# Check if Ollama service is running by querying it
retry=0
max_retries=5
until ollama list || [ $retry -ge $max_retries ]; do
    echo "Waiting for Ollama service to be ready... (retry: $retry)"
    sleep 5
    retry=$((retry + 1))
done

if [ $retry -ge $max_retries ]; then
    echo "Ollama service did not start. Exiting."
    exit 1
fi

echo "Ollama service is ready."

# Run the generate_commit script
git config --global --add safe.directory /usr/src/project
generate_commit
