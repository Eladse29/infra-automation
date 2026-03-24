from pydantic import BaseModel, field_validator
from ipaddress import IPv4Address
import random


class MachineConfig(BaseModel):
    name: str
    os: str
    cpu: int
    ram_gb: int
    public_ip: str | None = None

    @field_validator('name')
    @classmethod
    def name_validator(cls, v: str) -> str:
        if not (2 <= len(v) <= 20):
            raise ValueError("Name must be 2-20 chars")
        if not v.isalnum():
            raise ValueError("Name must be alphanumeric")
        return v

    @field_validator('os')
    @classmethod
    def os_validator(cls, v: str) -> str:
        valid_oses = ['ubuntu-24.04-lts', 'ubuntu-22.04-lts', 'debian-12', 'centos-8']
        normalized = v.lower().replace(" ", "-")
        if normalized not in valid_oses:
            raise ValueError(f"OS must be one of {valid_oses}")
        return normalized

    @field_validator('ram_gb')
    @classmethod
    def ram_validator(cls, v: int, info) -> int:
        cpu = info.data.get('cpu')
        valid_combos = {1: 2, 2: 4, 4: 8, 8: 16}
        if cpu and v != valid_combos.get(cpu):
            raise ValueError(f"CPU {cpu} requires {valid_combos[cpu]}GB RAM")
        return v

    @field_validator('public_ip')
    @classmethod
    def ip_validator(cls, v: str | None) -> str | None:
        if v is None:
            return None
        try:
            IPv4Address(v)
        except Exception:
            raise ValueError("public_ip must be a valid IPv4 address")
        return v


def generate_public_ip() -> str:
    """Generate a random IPv4 address (simulation only)."""
    # Avoid special ranges like 0, 127, 224-255
    octets = [
        random.randint(1, 223),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(1, 254),
    ]
    return ".".join(map(str, octets))