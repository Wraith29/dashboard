__all__ = ["Recipe"]

from dataclasses import dataclass
from typing import NotRequired, TypedDict

from bson import ObjectId

from src.models.recipes.ingredient import Ingredient


@dataclass
class Recipe(TypedDict):
    name: str
    description: str
    ingredients: list[Ingredient]
    instructions: list[str]
    tags: list[str]
    serves: int
    query_name: NotRequired[str]
    _id: NotRequired[ObjectId]


def query_name(recipe: Recipe) -> str:
    return recipe["name"].replace(" ", "-").lower()
