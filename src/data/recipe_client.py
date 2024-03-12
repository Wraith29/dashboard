__all__ = ["RecipeClient"]

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from src.config import Config
from src.models.recipe import Recipe, query_name


class RecipeClient:
    _client: MongoClient[Recipe]
    _db: Database[Recipe]

    def __init__(self) -> None:
        self._client = MongoClient(host=Config.mongodb_host, port=Config.mongodb_port)
        self._db = self._client["dashboard"]

    def get_collection(self) -> Collection[Recipe]:
        return self._db.get_collection("recipes")

    def insert_recipe(self, recipe: Recipe) -> None:
        collection = self.get_collection()
        recipe["query_name"] = query_name(recipe)

        collection.insert_one(recipe)

    def get_all_recipes(self) -> list[Recipe]:
        recipes: list[Recipe] = []

        all_recipes = self.get_collection().find()
        for recipe in all_recipes:
            recipes.append(recipe)

        return recipes

    def get_by_query_name(self, name: str) -> Recipe | None:
        value = self.get_collection().find_one({'query_name': name})

        if value is None:
            return None

        return value
