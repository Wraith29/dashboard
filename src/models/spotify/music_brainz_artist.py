__all__ = ["MusicBrainzArtist"]


from typing import TypedDict


class MusicBrainzArtist(TypedDict):
    """This contains only the required information returned from the Music Brainz API"""

    id: str
    name: str
