from pydantic import BaseModel
from pydantic import conint

class RatedSong(BaseModel):
    rating: conint(ge=1, le=5)