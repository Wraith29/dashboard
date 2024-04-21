__all__ = ["Ingredient"]

from dataclasses import dataclass
from typing import TypedDict


@dataclass
class Ingredient(TypedDict):
    name: str
    measurement: str
    quantity: int
