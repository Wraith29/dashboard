__all__ = ["MusicBrainzClient"]


import requests
from src.models.spotify.music_brainz_artist import MusicBrainzArtist


class MusicBrainzClient:
    base_url = "http://musicbrainz.org/ws/2"
    user_agent_string = "SetlistPlaylistGenerator/1.0.0 (i.acnaylor@gmail.com)"

    def _query(self, args: dict[str, str]) -> str:
        return "query=" + " and ".join([f"{k}:{v}" for k, v in args.items()])

    def search_artist_by_name(self, name: str) -> MusicBrainzArtist | None:
        query = self._query({"artist": name})
        url = f"{self.base_url}/artist/?{query}"

        response = requests.get(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": self.user_agent_string,
            },
        )

        items = response.json()

        if len(items) < 1:
            return None

        return items["artists"][0]
