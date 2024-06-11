# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make the generate_commit.py script executable
RUN chmod +x commit_generator/generate_commit.py

# Add /usr/local/bin to PATH for convenience
ENV PATH="/usr/local/bin:${PATH}"

# Create a symbolic link for the script
RUN ln -sf /usr/src/app/commit_generator/generate_commit.py /usr/local/bin/generate_commit

# Run generate_commit.py when the container launches
CMD ["generate_commit"]
