FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH="/"

# Working directory in the container
WORKDIR /app

# Copying the requirements file and installing dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copying the application code into the container
COPY ./log_analyzer /app/log_analyzer/

# Creating a volume for input and output files
VOLUME [ "/data" ]

# Setting the entrypoint to the CLI tool
ENTRYPOINT ["python", "-m", "log_analyzer.cli"]
