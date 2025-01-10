import random
import string
from typing import List, Optional, Any

from fastapi import FastAPI, HTTPException, Header, Query, Depends
from pydantic import BaseModel


class UserRegistration(BaseModel):
    name: str
    age: int


class Track(BaseModel):
    name: str
    artist: str
    year: Optional[int] = None
    genres: List[str] = []


app = FastAPI()
tracks: dict[int, Track] = {}
track_counter = 1
tokens: dict[str, str] = {}


def validate_token(x_token: Optional[str] = Header(None)) -> str:
    if not x_token:
        raise HTTPException(status_code=401, detail="Missing token")
    if x_token not in tokens.keys():
        raise HTTPException(status_code=401, detail="Incorrect token")
    return x_token


@app.post("/api/v1/registration/register_user")
def register_user(user: UserRegistration) -> dict[str, str]:
    token: str = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
    tokens[token] = user.name
    return {"token": token}


@app.post("/api/v1/tracks/add_track", status_code=201)
def add_track(
        track: Track,
        x_token: str = Depends(validate_token)
) -> dict[str, int]:
    global track_counter
    tracks[track_counter] = track
    track_counter += 1
    return {"track_id": track_counter - 1}


@app.get("/api/v1/tracks/all")
def get_all_tracks(x_token: str = Depends(validate_token)) -> list[dict[str, Any]]:
    return list(track.model_dump() for track in tracks.values())


@app.get("/api/v1/tracks/search")
def search_tracks(
        x_token: str = Depends(validate_token),
        name: Optional[str] = Query(None),
        artist: Optional[str] = Query(None),
) -> dict[str, list[Any]] | dict[str, list[int]]:
    if not name and not artist:
        raise HTTPException(status_code=422, detail="You should specify at least one search argument")
    if not tracks:
        return {"track_ids": []}
    return {"track_ids": [track_id for (track_id, track) in tracks.items()
                          if (not name or (name and name in track.name))
                          and (not artist or (artist and artist in track.artist))
                          ]}


@app.delete("/api/v1/tracks/{track_id}")
def delete_track(track_id: int, x_token: str = Depends(validate_token)) -> dict[str, str]:
    if track_id in tracks.keys():
        del tracks[track_id]
        return {"status": "track removed"}
    raise HTTPException(status_code=404, detail="Invalid track_id")


@app.get("/api/v1/tracks/{track_id}")
def get_track(track_id: int, x_token: str = Depends(validate_token)) -> dict[str, str]:
    if track_id in tracks.keys():
        track: dict[str, str] = tracks[track_id].model_dump()
        return {"name": track["name"], "artist": track["artist"]}
    raise HTTPException(status_code=404, detail="Invalid track_id")
