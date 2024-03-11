__all__ = ["home_bp"]

from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.get("/")
def home() -> str:
    return render_template("pages/home.html")


@home_bp.get("/not-found")
def not_found() -> tuple[str, int]:
    return (render_template("pages/not-found.html"), 404)
