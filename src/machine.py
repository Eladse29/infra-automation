from datetime import datetime
from typing import Any, Dict


class Machine:
    """
    מייצגת מכונה וירטואלית אחת במערכת.
    """

    def __init__(
        self,
        name: str,
        os: str,
        cpu: int,
        ram_gb: int,
        public_ip: str | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.name = name
        self.os = os
        self.cpu = cpu
        self.ram_gb = ram_gb
        self.public_ip = public_ip
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """
        מחזירה ייצוג מילון (dictionary) של המכונה,
        מתאים לכתיבה ל-JSON או ללוגים.
        """
        return {
            "name": self.name,
            "os": self.os,
            "cpu": self.cpu,
            "ram_gb": self.ram_gb,
            "public_ip": self.public_ip,
            "created_at": self.created_at.isoformat() + "Z",
        }

    def __repr__(self) -> str:
        return (
            f"Machine(name={self.name!r}, os={self.os!r}, "
            f"cpu={self.cpu}, ram_gb={self.ram_gb}, "
            f"public_ip={self.public_ip!r})"
        )
