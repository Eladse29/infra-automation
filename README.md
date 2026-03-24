# DevOps Infrastructure Provisioning & Configuration Automation

## Project Overview

This project is a **Python-based automation tool** that simulates infrastructure provisioning and service configuration.  
It allows users to define virtual machines (VMs), validates the input, stores configurations in JSON, logs actions, and simulates service installation using a Bash script.

---

## Features

- Accepts dynamic VM definitions from the user.
- Validates input (name, OS, CPU, RAM, public IP) using **Pydantic**.
- Stores VM configurations in `configs/instances.json`.
- Logs provisioning actions and errors in `logs/provisioning.log`.
- Simulates service installation via Bash (`scripts/install_nginx.sh`).
- Modular, class-based design (`Machine` class in `src/machine.py`).

---

## Project Structure
infra-automation/
├─ src/
│ ├─ infra_simulator.py # Main Python script
│ ├─ machine.py # Machine class
│ └─ input_validator.py # Pydantic validators
├─ scripts/
│ └─ install_nginx.sh # Bash script for simulating service installation
├─ configs/
│ └─ instances.json # VM definitions stored here
├─ logs/
│ └─ provisioning.log # Logs actions and errors
├─ .venv/ # Python virtual environment
├─ requirements.txt # Python dependencies
└─ README.md


---

## Requirements

- Python 3.14+  
- Bash (for running service simulation, works on Linux/WSL/macOS)  
- Python packages: see `requirements.txt`

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt


How to Run

Run the main script from the project root:

python -m src.infra_simulator

You will be prompted for:

VM Name – 2-20 alphanumeric characters

OS – must be one of: ubuntu-24.04-lts, ubuntu-22.04-lts, debian-12, centos-8

CPU cores – allowed: 1, 2, 4, 8

RAM GB – must match CPU (1→2, 2→4, 4→8, 8→16)

Public IP – y/n or yes/no

After input, the tool will:

Create a Machine object

Save it to configs/instances.json

Log all actions in logs/provisioning.log

Run the Bash script to simulate service installation