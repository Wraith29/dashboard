__all__ = ["recipe_bp"]

import json
from flask import Blueprint, request
from src.data.recipe_client import RecipeClient
from src.models.recipes.recipe import Recipe

recipe_bp = Blueprint("recipe", __name__, url_prefix="recipe")


@recipe_bp.get("/<string:name>")
def get_recipe(name: str) -> tuple[Recipe | dict[str, str], int]:
    recipe = RecipeClient().get_by_query_name(name)

    if recipe is None:
        return ({}, 404)

    return (recipe, 200)


@recipe_bp.post("/create")
def create() -> tuple[str, int]:
    client = RecipeClient()

    body = request.data
    body_obj: Recipe = json.loads(body)

    try:
        client.insert_recipe(body_obj)
    except Exception as e:
        return f"Error Creating Recipe: {e}", 500

    return "", 200


@recipe_bp.put("/<string:name>/add-tag")
def add_tag(name: str) -> tuple[list[str], int]:
    tag = json.loads(request.data)["tag"]
    client = RecipeClient()

    if tag == "":
        return ([], 400)

    tags = client.add_tag_to_recipe(name, tag)

    return (tags, 200)
