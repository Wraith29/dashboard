__all__ = ["RecipeClient"]

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from src.config import Config
from src.models.recipe import Recipe


class RecipeClient:
    _client: MongoClient
    _db: Database

    def __init__(self) -> None:
        self._client = MongoClient(host=Config.mongodb_host, port=Config.mongodb_port)
        self._db = self._client["dashboard"]

    def get_collection(self) -> Collection:
        return self._db.get_collection("recipes")

    def insert_recipe(self, recipe: Recipe) -> None:
        collection = self.get_collection()

        json_value = recipe.to_dict()

        collection.insert_one(json_value)

    def get_all_recipes(self) -> list[Recipe]:
        recipes: list[Recipe] = []

        all_recipes = self.get_collection().find()
        for recipe in all_recipes:
            recipes.append(Recipe.from_dict(recipe))

        return recipes

    def get_by_query_name(self, name: str) -> Recipe | None:
        value = self.get_collection().find_one({'query_name': name})

        if value is None:
            return None

        return Recipe.from_dict(value)
