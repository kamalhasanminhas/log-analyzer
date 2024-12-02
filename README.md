# Log Analyzer CLI Tool

A simple command-line tool for analyzing log files. Supports various analysis options such as identifying the most and least frequent IPs, calculating total bytes exchanged, and events per second.

## Features

- Extensible design following SOLID principles.
- Outputs results in JSON format.
- Fault-tolerant parsing and processing.
- Dockerized for easy deployment.

## Requirements

- **Python**: >= 3.11
- **Dependencies**: See `pyproject.toml`
- **Docker**: Optional, for containerized deployment.

## Installation
```bash
make install
```

Or

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Run analysis

```bash
make run ARGS="log_file_1.log log_file_2.log output.json --mfip --lfip --eps --bytes"
```

### Using Python
```bash
python log_analyzer/cli.py log_file_1.log log_file_2.log output.json --mfip --lfip --eps --bytes
```

### Using Docker
Build docker image
```bash
docker build -t log-analyzer .
```

Run analyzer inside the container
Copy `access.log` to `.data` directory and mount it
```bash
docker run --rm -v $(pwd)/.data:/data log-analyzer /data/access.log /data/results.json --mfip --bytes --lfip --eps
```


### Running tests
```bash
make test
```


### Building Package
Please make sure you have installed the `dev-requirements.txt`

```bash
make build
```
