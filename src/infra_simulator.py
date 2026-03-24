#!/usr/bin/env python3
import os
import json
import logging
import subprocess
from src.input_validator import MachineConfig, generate_public_ip
from src.machine import Machine

# ------------------------
# הגדרות בסיסיות
# ------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "configs", "instances.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "provisioning.log")

# הגדרת logging
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

# ------------------------
# קלט משתמש
# ------------------------
def get_user_input() -> MachineConfig:
    print("=== VM Provisioning ===")
    print("Valid OS examples: ubuntu-24.04-lts, ubuntu-22.04-lts, debian-12, centos-8")

    # שם VM
    while True:
        name = input("VM name (2-20 chars, letters+digits): ").strip()
        try:
            vm_name = MachineConfig(name=name, os="ubuntu-22.04-lts", cpu=1, ram_gb=2).name
            break
        except Exception:
            print("❌ Invalid name. Use 2-20 letters/digits only")

    # מערכת הפעלה
    valid_oses = ['ubuntu-24.04-lts', 'ubuntu-22.04-lts', 'debian-12', 'centos-8']
    while True:
        os_type = input(f"OS {valid_oses}: ").strip()
        if os_type.lower().replace(" ", "-") in valid_oses:
            os_type = os_type.lower().replace(" ", "-")
            break
        else:
            print("❌ Invalid OS")

    # CPU
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

    # יצירת MachineConfig עם ולידציה
    vm_config = MachineConfig(
        name=name,
        os=os_type,
        cpu=cpu,
        ram_gb=ram,
        public_ip=public_ip
    )
    return vm_config

# ------------------------
# שמירת VM ל-JSON
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

    logging.info(f"Saved VM '{machine.name}' to {CONFIG_PATH}")
    print(f"✓ Machine '{machine.name}' created successfully")
    print(f"✓ Saved VM to {CONFIG_PATH}")

# ------------------------
# קריאה ל-Bash Script להתקנת שירות
# ------------------------
def install_service():
    script_path = os.path.join(BASE_DIR, "scripts", "install_nginx.sh")
    try:
        subprocess.run(["bash", script_path], check=True)
        logging.info("Service installation script executed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Service installation failed: {e}")

# ------------------------
# Main
# ------------------------
def main() -> None:
    try:
        vm_config = get_user_input()

        # המרה מ-Pydantic model למחלקת Machine
        machine = Machine(
            name=vm_config.name,
            os=vm_config.os,
            cpu=vm_config.cpu,
            ram_gb=vm_config.ram_gb,
            public_ip=vm_config.public_ip
        )

        save_machine(machine)
        install_service()

    except Exception as e:
        logging.error(f"Error during provisioning: {e}")
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()