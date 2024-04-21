__all__ = ["setlist_bp"]

import logging
from json import dumps

import time
from flask import Blueprint, Response, render_template, request, session

from src.data.spotify_client import SpotifyClient

setlist_bp = Blueprint("setlist", __name__, url_prefix="/setlist-generator")


@setlist_bp.post("/create-setlist")
def create_setlist() -> Response | tuple[str, int]:
    # TODO: Get rid of all the `# type: ignore`s
    artist_name = request.get_json()["name"]
    logger = logging.getLogger()
    logger.debug("Creating Spotify Client")

    if "spotify_token" in session.keys():
        expires_at = float(session.get("spotify_token_expires_at"))  # type: ignore

        if time.time() < expires_at:
            spotify_client = SpotifyClient(session.get("spotify_token"))  # type: ignore

            spotify_client.create_setlist_playlist_for_artist(artist_name)
            return render_template("pages/setlist-generator/index.html"), 200

        session.pop("spotify_token")  # type: ignore
        session.pop("spotify_token_expires_at")  # type: ignore

    if "artist_name" in session:
        session.pop("artist_name")  # type: ignore
    session["artist_name"] = artist_name

    url = SpotifyClient.get_auth_url()

    logger.debug(f"Spotify Token not found. Redirecting to {url} to login.")

    return Response(
        dumps({"redirect_uri": url}), 200, {"Content-Type": "application/json"}
    )
