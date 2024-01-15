# 'Dockerfile' is also valid. However, if a 'Containerfile' and 'Dockerfile' are both in
# the context directory, Podman will instead use 'Containerfile', ignoring the 'Dockerfile'.

# Use no higher than Python 3.11 for Tensorflow use.
FROM python:3.11-slim

# Create a non-root user to run the application
RUN adduser --disabled-password --gecos '' myuser 

# Set working directory inside the container
WORKDIR /app

# Create and activate a virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Copy the content of the local src directory to the working directory
COPY . .

# Upgrade pip and install python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt 
# Install nodejs, npm, and yarn
RUN apt-get update && apt-get install -y nodejs npm && npm install -g yarn

# Install node dependencies
WORKDIR /app/frontend
RUN yarn install && yarn playwright install-deps
WORKDIR /app

# Clean up unnecessary files
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Switch to the non-root user
USER myuser