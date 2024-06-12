FROM python:3.12-slim

# Dummy argument to force cache busting
ARG CACHEBUST=1

WORKDIR /usr/src/app

# Install Git and other dependencies
RUN apt-get update && \
    apt-get install -y git curl && \
    rm -rf /var/lib/apt/lists/* && \
    echo "Git installed successfully"

# Install Ollama CLI
RUN curl -sSL https://ollama.com/install.sh | bash

# Install wait-for-it
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Make the generate_commit script executable
RUN chmod +x commit_generator/generate_commit.py
RUN ln -sf /usr/src/app/commit_generator/generate_commit.py /usr/local/bin/generate_commit

# Serving Ollama
#RUN ollama serve

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
