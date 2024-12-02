# Define paths and variables
PYTHONPATH := $(shell pwd)
VENV_DIR = .venv

# Python and pip commands for virtualenv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
ACTIVATE = $(VENV_DIR)/bin/activate

# Default target: help
.DEFAULT_GOAL := help

# List all available commands
help:
	@echo "Available commands:"
	@echo "  make venv         - Set up the environment"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run all tests"
	@echo "  make run          - Run the Log Analyzer CLI tool"
	@echo "  make clean        - Clean up temporary files"
	@echo "  make build        - Build python package"


# Target to create a virtual environment
.PHONY: venv
venv:
	@echo "Checking if virtual environment exists..."
	if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Setting up virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
		echo "Virtual environment created at $(VENV_DIR)"; \
	else \
		echo "Virtual environment already exists."; \
	fi


# Target to install dependencies from requirements.txt
.PHONY: install
install: venv
	@echo "Installing dependencies from requirements.txt..."
	. $(ACTIVATE) && $(PIP) install -r requirements.txt
	@echo "Dependencies installed."


# Run tests
.PHONY: test
test:
	PYTHONPATH=$(PYTHONPATH) coverage run -m unittest discover
	coverage report


# Run the main Log Analyzer tool
.PHONY: run
run:
	@echo "Running the Log Analyzer tool..."
	@PYTHONPATH=$(PYTHONPATH) . $(ACTIVATE) && python log_analyzer/cli.py $(ARGS)

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -exec rm -f {} +
	@find . -type d -name "log_analyzer.egg-info" -exec rm -rf {} +
	@rm -rf dist
	@echo "Cleaned!"

# Example usage message
example:
	@echo "To run the tool, use: make run ARGS='logs/access.log results.json --mfip --lfip --eps --bytes'"


# Build package
build:
	@python -m build
