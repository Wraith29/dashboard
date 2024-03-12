__all__ = ["Ingredient"]

from dataclasses import dataclass
from typing import TypedDict


@dataclass
class Ingredient(TypedDict):
    name: str
    measurement: str
    quantity: int

    # def to_dict(self) -> dict[str, str | int]:
    #     if self.display_text is None:

    #     return {
    #         "name": self.name,
    #         "measurement": self.measurement,
    #         "quantity": self.quantity,
    #         "display_text": self.display_text
    #     }

    # @staticmethod
    # def from_dict(obj: dict[str, Any]) -> 'Ingredient':
    #     return Ingredient(**obj)
