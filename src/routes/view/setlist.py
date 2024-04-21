__all__ = ["setlist_bp"]

import logging

import time
from datetime import datetime
import requests
from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug import Response

from src.config import Config

setlist_bp = Blueprint("setlist", __name__, url_prefix="/setlist-generator")


@setlist_bp.get("/")
def setlist_generator() -> tuple[str, int]:
    if "token_refresh" in request.args:
        if "artist_name" in session:
            artist_name: str = session.get("artist_name")
            if type(artist_name) is not str:
                raise ValueError("Artist Name is an invalid type")
            requests.get("api/setlist-generator/create-setlist", json={"artist_name": artist_name})

        return render_template("pages/setlist-generator/index.html", refresh=True), 200

    return render_template("pages/setlist-generator/index.html"), 200


@setlist_bp.get("/auth")
def auth() -> Response:
    logger = logging.getLogger()
    code = request.args.get("code")

    logger.debug(f"Request Args: {request.args}")

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "code": code,
            "redirect_uri": Config.spotify["redirect_uri"],
            "grant_type": "authorization_code",
            "client_id": Config.spotify["client_id"],
            "client_secret": Config.spotify["client_secret"],
        },
        json=True,
    )

    response_data = response.json()

    access_token = response_data["access_token"]
    now = time.time()
    expires_at = now + int(response_data["expires_in"])
    logger.debug(f"Spotify Token Expires At: {datetime.fromtimestamp(expires_at)}")

    session["spotify_token"] = access_token
    session["spotify_token_expires_at"] = expires_at

    return redirect(f"{url_for("view.setlist.setlist_generator")}?token_refresh=true")
