__all__ = ["SpotifyClient"]


from asyncio import gather
import operator
from dataclasses import dataclass
from logging import Logger, getLogger

from httpx import AsyncClient, Response
import requests
from result import Err, Ok, Result

from src.config import Config
from src.data.music_brainz_client import MusicBrainzClient
from src.data.setlist_client import SetlistClient
from src.models.spotify.setlist import Setlist
from src.models.spotify.setlist_track import SetlistTrack


@dataclass
class Track:
    name: str
    positions: list[int]

    def get_avg_position(self) -> int:
        return int(sum(self.positions) / len(self.positions))


class SpotifyClient:
    base_url = "https://api.spotify.com/v1"
    scope = (
        "user-read-private "
        "user-read-email "
        "playlist-modify-public "
        "playlist-modify-private"
    )
    state: str
    token: str
    music_brainz_client: MusicBrainzClient
    setlist_client: SetlistClient
    logger: Logger

    def __init__(self, token: str) -> None:
        self.state = Config.spotify["state"]
        self.token = token
        self.music_brainz_client = MusicBrainzClient()
        self.setlist_client = SetlistClient()
        self.logger = getLogger()

    @staticmethod
    def get_auth_url() -> str:
        query_args = {
            "response_type": "code",
            "client_id": Config.spotify["client_id"],
            "scope": SpotifyClient.scope,
            "redirect_uri": Config.spotify["redirect_uri"],
            "state": Config.spotify["state"],
        }

        query_str = ""

        for key, value in query_args.items():
            query_str += f"{key}={value}&"

        query_str = query_str[:-1]

        return f"https://accounts.spotify.com/authorize?{query_str}"

    def get_setlists(self, artist_name: str) -> Result[list[Setlist], str]:
        self.logger.debug(f"Searching for {artist_name}'s setlists")
        artist_mbid = self.music_brainz_client.search_artist_by_name(artist_name)

        if isinstance(artist_mbid, Err):
            self.logger.error(f"Error retrieving Artist MBID {artist_mbid.err()}")
            return Err(artist_mbid.err())

        mbid = artist_mbid.ok()

        setlists = self.setlist_client.get_setlists_for_artist(mbid["id"])
        if isinstance(setlists, Err):
            self.logger.error(f"Error getting artist's setlists {setlists}")
            return Err(setlists.err())

        setlists_with_tour_and_date = list(
            sorted(
                filter(lambda sl: "tour" in sl and "eventDate" in sl, setlists.ok()),
                key=operator.itemgetter("eventDate"),
                reverse=True,
            )
        )

        if len(setlists_with_tour_and_date) < 1:
            self.logger.error(f"No Setlists found for {artist_name}")
            return Err(f"No Setlists found for {artist_name}")

        return Ok(setlists_with_tour_and_date)

    def get_most_recent_tour_name(self, setlists: list[Setlist]) -> Result[str, str]:
        if len(setlists) < 1:
            return Err("No Setlists Found")

        most_recent_setlist = setlists[0]

        if "tour" not in most_recent_setlist or "name" not in most_recent_setlist["tour"]:
            return Err(f"No Tour found in {most_recent_setlist}")

        most_recent_tour = most_recent_setlist["tour"]["name"]

        return Ok(most_recent_tour)

    def get_setlists_on_most_recent_tour(
        self, artist_name: str
    ) -> Result[tuple[list[Setlist], str], str]:
        setlists = self.get_setlists(artist_name)
        if isinstance(setlists, Err):
            self.logger.error(f"Error Getting Setlists {setlists.err()}")
            return Err(setlists.err())

        tour = self.get_most_recent_tour_name(setlists.ok())
        if isinstance(tour, Err):
            return Err(tour.err())

        tour_name = tour.ok()

        return Ok((list(filter(lambda sl: sl["tour"]["name"] == tour_name, setlists.ok())), tour_name))

    def get_tracklist_in_order(self, setlists: list[Setlist]) -> list[str]:
        tracks: dict[str, Track] = {}

        for setlist in setlists:
            for sl in setlist["sets"]["set"]:
                for idx, song in enumerate(sl["song"]):
                    song_name = song["name"]
                    if song_name in tracks:
                        tracks[song_name].positions.append(idx + 1)
                    else:
                        tracks[song_name] = Track(song_name, [idx + 1])

        track_list = list(filter(lambda t: t.name != "", tracks.values()))

        track_pos = {track.name: track.get_avg_position() for track in track_list}

        ordered_tracks = list(
            map(operator.itemgetter(0), sorted(track_pos.items(), key=operator.itemgetter(1)))
        )

        return ordered_tracks

    def get_user_id(self) -> Result[str, str]:
        url = f"{self.base_url}/me"

        response = requests.get(
            url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
        )

        if not response.ok:
            self.logger.error(f"Error getting user id: {response.json()}")
            return Err(f"Error getting user id: {response.json()}")

        response_data = response.json()

        if "id" not in response_data:
            self.logger.error("User id not found")
            return Err("User id not found")

        return Ok(response_data["id"])

    def create_playlist(self, artist_name: str, tour_name: str) -> Result[str, str]:
        """Returns the ID of the created playlist"""
        user_id_request = self.get_user_id()
        if isinstance(user_id_request, Err):
            self.logger.error(user_id_request.err())
            return Err(user_id_request.err())

        user_id = user_id_request.ok()

        url = f"{self.base_url}/users/{user_id}/playlists"
        desc = (
            "Playlist Generated by "
            "https://github.com/Wraith29/dashboard?tab=readme-ov-file#setlist-generator"
        )

        response = requests.post(
            url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
            json={
                "name": f"{artist_name}: {tour_name}",
                "description": desc,
                "public": False,
            },
        )

        response_data = response.json()

        if response.status_code == 201 and "id" in response_data:
            return Ok(response_data["id"])

        # TODO: Improve the usability of this
        # TODO: Currently doesn't give any info to the user
        return Err(f"Error creating Playlist: {response.json()}")

    async def get_async(self, url: str) -> Response:
        async with AsyncClient() as client:
            return await client.get(url, headers={
                "Accept": "application/json",
                "Content-Type": "applcation/json",
                "Authorization": f"Bearer {self.token}"
            })

    # TODO: Make this perform better
    # Ideas:
    #  - query artist, then albums, and find tracks that way
    #  - consider multi-threading? is that even possible lol
    async def get_track_ids(
        self, artist_name: str, track_names: list[str]
    ) -> Result[list[SetlistTrack], list[str]]:
        url = f"{self.base_url}/search"

        track_ids: list[SetlistTrack] = []
        errors: list[str] = []

        track_urls = [f"{url}?q=track:{track}+artist:{artist_name}&type=track" for track in track_names]
        tasks = [self.get_async(track_url) for track_url in track_urls]

        responses = await gather(*tasks)

        for response in responses:
            if not response.is_success:
                errors.append(f"Error quering track: {response.json()}")
                continue

            response_data = response.json()
            if "tracks" not in response_data:
                errors.append(f"Tracks not found in {response_data}")
                continue

            tracks = response_data["tracks"]
            if "items" not in tracks or len(tracks["items"]) < 1:
                errors.append(f"Items not found in {response_data}")
                continue

            first_item = tracks["items"][0]

            track_ids.append({"name": first_item["name"], "id": first_item["id"]})

        return Ok(track_ids)

    async def add_tracks_to_playlist(
        self, artist_name: str, playlist_id: str, tracks: list[str]
    ) -> Result[None, str]:
        url = f"{self.base_url}/playlists/{playlist_id}/tracks"

        track_ids = await self.get_track_ids(artist_name, tracks)
        if isinstance(track_ids, Err):
            errors = ','.join(track_ids.err())
            self.logger.error(errors)
            return Err(errors)

        track_uris = ",".join([f"spotify:track:{track["id"]}" for track in track_ids.ok()])

        response = requests.post(f"{url}?uris={track_uris}", headers={
            "Accept": "Application/json",
            "Authorization": f"Bearer {self.token}"
        })

        response_data = response.json()

        if "error" in response_data:
            self.logger.error(f"Error Creating Playlist: {response.json()["error"]["message"]}")

        return Ok(None)

    async def create_setlist_playlist_for_artist(self, artist_name: str) -> Result[str, str]:
        self.logger.debug(f"Creating playlist for {artist_name}")

        setlists_on_tour = self.get_setlists_on_most_recent_tour(artist_name)
        if isinstance(setlists_on_tour, Err):
            self.logger.error("Error getting setlists for tour")
            return Err(f"Error getting setlists for tour {setlists_on_tour.err()}")

        setlists, tour_name = setlists_on_tour.ok()

        track_list = self.get_tracklist_in_order(setlists)

        playlist_id = self.create_playlist(artist_name, tour_name)
        if isinstance(playlist_id, Err):
            self.logger.error(f"Error creating playlist: {playlist_id.err()}")
            return Err(playlist_id.err())

        success = await self.add_tracks_to_playlist(artist_name, playlist_id.ok(), track_list)
        if isinstance(success, Err):
            self.logger.error(success.err())
            return Err(success.err())

        return Ok(playlist_id.ok())
