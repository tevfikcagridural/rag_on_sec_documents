# Use Python 3.11 as base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container at /src
COPY requirements.txt /src/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade --no-cache-dir --force-reinstall -r requirements.txt

# Copy the current directory contents into the container at /src
COPY /src /src
COPY data/processed src/data/processed

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Healtcheck
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

# Run
ENTRYPOINT ["streamlit", "run", "main.py", "--browser.serverAddress", "0.0.0.0", "--browser.gatherUsageStats", "false", "--server.port", "8080"]