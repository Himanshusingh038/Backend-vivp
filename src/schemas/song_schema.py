from pydantic import BaseModel
from typing import Optional
from pydantic import conint

class Song(BaseModel):
    id: str
    title: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int
    num_bars: int
    num_sections: int
    num_segments: int
    class_: int
    rating: Optional[conint(ge=1, le=5)] = None

    class Config:
        from_attributes = True
