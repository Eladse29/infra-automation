#!/usr/bin/env python3
import os
import json
import logging
import subprocess
from src.input_validator import MachineConfig, generate_public_ip
from src.machine import Machine

# ------------------------
# Base directories
# ------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "configs", "instances.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "provisioning.log")

# ------------------------
# Logging setup
# ------------------------
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

# ------------------------
# User input
# ------------------------
def get_user_input() -> MachineConfig:
    print("=== VM Provisioning ===")
    print("Valid OS examples: ubuntu-24.04-lts, ubuntu-22.04-lts, debian-12, centos-8")

    # VM name
    while True:
        name = input("VM name (2-20 chars, letters+digits): ").strip()
        try:
            MachineConfig(name=name, os="ubuntu-22.04-lts", cpu=1, ram_gb=2)
            break
        except Exception:
            print("❌ Invalid name. Use 2-20 letters/digits only")

    # OS type
    valid_oses = ['ubuntu-24.04-lts', 'ubuntu-22.04-lts', 'debian-12', 'centos-8']
    while True:
        os_type = input(f"OS {valid_oses}: ").strip().lower().replace(" ", "-")
        if os_type in valid_oses:
            break
        else:
            print("❌ Invalid OS")

    # CPU cores
    valid_cpus = [1, 2, 4, 8]
    while True:
        try:
            cpu = int(input(f"CPU cores {valid_cpus}: ").strip())
            if cpu in valid_cpus:
                break
            else:
                print("❌ Invalid CPU value")
        except ValueError:
            print("❌ Please enter a number")

    # RAM
    valid_combos = {1:2, 2:4, 4:8, 8:16}
    while True:
        try:
            ram = int(input(f"RAM GB (CPU {cpu} → {valid_combos[cpu]}GB): ").strip())
            if ram == valid_combos[cpu]:
                break
            else:
                print(f"❌ CPU {cpu} requires {valid_combos[cpu]}GB RAM")
        except ValueError:
            print("❌ Please enter a number")

    # Public IP
    while True:
        needs_ip = input("Need public IP? (y/n or yes/no): ").strip().lower()
        if needs_ip in ["y", "yes"]:
            public_ip = generate_public_ip()
            break
        elif needs_ip in ["n", "no"]:
            public_ip = None
            break
        else:
            print("❌ Please enter y/n/yes/no")

    # Create Pydantic model
    vm_config = MachineConfig(
        name=name,
        os=os_type,
        cpu=cpu,
        ram_gb=ram,
        public_ip=public_ip
    )
    return vm_config

# ------------------------
# Save VM to JSON
# ------------------------
def save_machine(machine: Machine) -> None:
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            instances = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        instances = []

    instances.append(machine.to_dict())

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(instances, f, indent=2, ensure_ascii=False)

    logging.info(f"Created machine object: {machine}")
    logging.info(f"Saved VM to JSON: {machine.to_dict()}")
    print(f"✓ Machine '{machine.name}' created successfully")
    print(f"✓ Saved VM to {CONFIG_PATH}")

# ------------------------
# Run Bash Script (optional)
# ------------------------
def run_bash_script():
    script_path = os.path.join(BASE_DIR, "scripts", "install_nginx.sh")
    
    if os.name == "nt":
        print("Service installation skipped on Windows. Run Bash script manually in WSL.")
        logging.info("Windows detected: Bash script skipped.")
        return

    if not os.path.exists(script_path):
        print(f"[WARNING] Bash script not found: {script_path}")
        logging.warning(f"Bash script not found: {script_path}")
        return

    try:
        subprocess.run(["bash", script_path], check=True)
        logging.info("Service installation script executed successfully")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Service installation failed: {e}")
        logging.error(f"Service installation failed: {e}")

# ------------------------
# Main
# ------------------------
def main() -> None:
    try:
        logging.info("=== Starting VM provisioning ===")
        vm_config = get_user_input()

        # Convert Pydantic model to Machine object
        machine = Machine(
            name=vm_config.name,
            os=vm_config.os,
            cpu=vm_config.cpu,
            ram_gb=vm_config.ram_gb,
            public_ip=vm_config.public_ip
        )

        save_machine(machine)
        run_bash_script()
        logging.info("=== VM provisioning finished ===")

    except Exception as e:
        logging.error(f"Error during provisioning: {e}")
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()