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
    def name_validator(cls, v):
        if not (2 <= len(v) <= 20):
            raise ValueError("Name must be 2-20 chars")
        if not v.isalnum():
            raise ValueError("Name must be alphanumeric")
        return v

    @field_validator('os')
    @classmethod
    def os_validator(cls, v):
        valid = [
    'ubuntu-24.04-lts',
    'ubuntu-22.04-lts',
    'debian-12',
    'centos-8'
]
        v = v.lower()
        if v not in valid:
            raise ValueError(f"OS must be one of {valid}")
        return v

    @field_validator('ram_gb')
    @classmethod
    def ram_validator(cls, v, info):
        cpu = info.data.get('cpu')
        valid = {1: 2, 2: 4, 4: 8, 8: 16}

        if cpu and v != valid.get(cpu):
            raise ValueError(f"CPU {cpu} requires {valid[cpu]}GB RAM")
        return v

    @field_validator('public_ip')
    @classmethod
    def ip_validator(cls, v):
        if v is None:
            return v
        IPv4Address(v)
        return v


def generate_public_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))