__all__ = ["view_bp"]

from flask import Blueprint

from src.routes.view.home import home_bp
from src.routes.view.recipe import recipe_bp


view_bp = Blueprint("view", __name__)

view_bp.register_blueprint(home_bp)
view_bp.register_blueprint(recipe_bp)
