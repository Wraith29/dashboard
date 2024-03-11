__all__ = ["recipe_bp"]

from flask import Blueprint, redirect, render_template, url_for
from werkzeug import Response

from src.data.recipe_client import RecipeClient


recipe_bp = Blueprint("recipe", __name__, url_prefix="/recipe-manager")


@recipe_bp.get("/")
def recipe_manager() -> tuple[str, int]:
    recipes = RecipeClient().get_all_recipes()

    return (
        render_template("pages/recipe-manager/index.html", recipes=recipes),
        200
    )


@recipe_bp.get("/create-recipe")
def create_recipe() -> tuple[str, int]:
    return (render_template("pages/recipe-manager/create.html"), 200)


@recipe_bp.get("/<string:recipe_name>")
def recipe(recipe_name: str) -> tuple[str, int] | Response:
    recipe = RecipeClient().get_by_query_name(recipe_name)

    if recipe is None:
        return redirect(url_for('view.home.not_found'))

    return (
        render_template("pages/recipe-manager/recipe.html", recipe=recipe),
        200
    )
