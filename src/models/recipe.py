__all__ = ["Recipe"]

from dataclasses import dataclass
from typing import Any

from bson import ObjectId

from src.models.ingredient import Ingredient


@dataclass
class Recipe:
    name: str
    description: str
    ingredients: list[Ingredient]
    instructions: list[str]
    tags: list[str]
    serves: int
    query_name: str | None = None
    _id: ObjectId | None = None

    def get_query_name(self) -> str:
        query_name = self.name.replace(" ", "-").lower()

        return query_name

    def to_dict(self) -> dict[str, str | list[dict[str, str | int]] | list[str] | int]:
        ingredients = [ing.to_dict() for ing in self.ingredients]

        return {
            "name": self.name,
            "description": self.description,
            "ingredients": ingredients,
            "instructions": self.instructions,
            "tags": self.tags,
            "serves": self.serves,
            "query_name": self.get_query_name()
        }

    @staticmethod
    def from_dict(obj: dict[str, Any]) -> 'Recipe':
        ingredients = [Ingredient.from_dict(ing) for ing in (obj["ingredients"])]
        del obj["ingredients"]

        return Recipe(
            ingredients=ingredients,
            **obj
        )
