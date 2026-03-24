
# Infrastructure Automation Project

## Overview
This project simulates virtual machine provisioning using Python.  
It validates user input, logs all operations, stores configurations in JSON format, and optionally runs a Bash script to install a basic service (Nginx).

---

## Features
- User input validation using Pydantic
- Structured logging of all operations (success and errors)
- Persistent storage of VM configurations in JSON
- Bash script integration for service installation
- Cross-platform support (Windows / Linux / WSL)

---

## Project Structure
```

infra-automation/
├── src/
│   ├── infra_simulator.py
│   ├── input_validator.py
│   └── machine.py
├── configs/
│   └── instances.json
├── logs/
│   └── provisioning.log
├── scripts/
│   └── install_nginx.sh

```

---

## Requirements
- Python 3.10+
- pip install pydantic
- (Optional) WSL or Linux environment for Bash script execution
- Install dependencies with:
```
pip install -r requirements.txt
```
---

## How to Run

### 1. Run the simulator
From the project root directory:

```

python -m src.infra_simulator

```

### 2. Provide input
Follow the prompts:
- VM name (2–20 alphanumeric characters)
- Operating system (from predefined list)
- CPU cores
- RAM (must match CPU requirements)
- Public IP (yes/no)

### 3. Output
- VM data is saved to:
```

configs/instances.json

```
- Logs are written to:
```

logs/provisioning.log

```

---

## Bash Script (Nginx Installation)

The project includes a Bash script that installs Nginx.

### On Linux / WSL
The script runs automatically after provisioning.

### On Windows
The script is skipped automatically.

To run manually in WSL:
```

bash scripts/install_nginx.sh

```

---

## Notes
- If `instances.json` does not exist, it will be created automatically.
- If the file is corrupted or empty, it will be reset.
- Bash execution is optional and does not affect the core functionality.

---

## Summary
This project demonstrates:
- Input validation
- Logging and error handling
- File-based persistence (JSON)
- Integration between Python and Bash using subprocess
