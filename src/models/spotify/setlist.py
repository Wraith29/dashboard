__all__ = ["Setlist"]


from typing import TypedDict


class SetlistTour(TypedDict):
    name: str


class SetlistSong(TypedDict):
    name: str
    info: str | None


class SetlistSet(TypedDict):
    song: list[SetlistSong]
    encore: int | None


class SetlistSets(TypedDict):
    set: list[SetlistSet]


class Setlist(TypedDict):
    """Similar to MusicBrainzArtist, only contains the data I actually need to use"""

    id: str
    eventDate: str
    tour: SetlistTour
    sets: SetlistSets
