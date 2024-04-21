__all__ = ["SetlistClient"]


from logging import Logger, getLogger

import requests
from result import Err, Ok, Result

from src.config import Config
from src.models.spotify.setlist import Setlist


class SetlistClient:
    logger: Logger
    base_url = "https://api.setlist.fm/rest/1.0"
    api_key: str

    def __init__(self) -> None:
        self.logger = getLogger()
        self.api_key = Config.setlist["api_key"]

    def get_setlists_for_artist(self, artist_id: str) -> Result[list[Setlist], str]:
        # TODO: Upgrade to check all pages, rather than just the first
        url = f"{self.base_url}/search/setlists"
        query = f"?artistMbid={artist_id}&countryCode=GB&page=1"

        response = requests.get(
            url + query,
            headers={"x-api-key": self.api_key, "Accept": "application/json"},
        )

        if not response.ok:
            self.logger.error(f"Error querying Setlist.fm: {response}")
            return Err("Error querying setlist.fm")

        setlist_data = response.json()

        if "setlist" not in setlist_data:
            self.logger.error("Setlists not found")
            return Err("Setlists not found")

        return Ok(setlist_data["setlist"])
