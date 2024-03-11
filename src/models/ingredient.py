__all__ = ["Ingredient"]

from dataclasses import dataclass
from typing import Any


@dataclass
class Ingredient:
    name: str
    measurement: str
    quantity: int
    display_text: str | None = None

    def to_dict(self) -> dict[str, str | int]:
        if self.display_text is None:
            self.display_text = f"{self.name} - {self.quantity} {self.measurement}"  # This may need revising in future

        return {
            "name": self.name,
            "measurement": self.measurement,
            "quantity": self.quantity,
            "display_text": self.display_text
        }

    @staticmethod
    def from_dict(obj: dict[str, Any]) -> 'Ingredient':
        return Ingredient(**obj)
