__all__ = ['recipe_bp']

import json
from typing import Any
from flask import Blueprint, request
from src.data.recipe_client import RecipeClient
from src.models.recipe import Recipe

recipe_bp = Blueprint('recipe', __name__, url_prefix='recipe')


@recipe_bp.get('/<string:name>')
def get_recipe(name: str) -> tuple[dict[str, Any], int]:
    recipe = RecipeClient().get_by_query_name(name)

    if recipe is None:
        return ({}, 404)

    return (recipe.to_dict(), 200)


@recipe_bp.post('/create')
def create() -> tuple[str, int]:
    client = RecipeClient()

    body = request.data
    body_obj = json.loads(body)

    recipe = Recipe.from_dict(body_obj)

    try:
        client.insert_recipe(recipe)
    except Exception as e:
        return f"Error Creating Recipe: {e}", 500

    return "", 200
