__all__ = ['api_bp']

from flask import Blueprint

from src.routes.api.recipe import recipe_bp


api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(recipe_bp)
