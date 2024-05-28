from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import Song as SongModel
from src.schemas.song_schema import Song
from src.schemas.rate_song_schema import RatedSong
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions import SongNotFoundException, DatabaseException

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/songs",
    tags=["songs"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get_songs", response_model=List[Song])
def get_songs(page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    try:
        offset = (page - 1) * per_page
        songs = db.query(SongModel).offset(offset).limit(per_page).all()
        if not songs:
            raise SongNotFoundException()
        return songs
    except SQLAlchemyError as e:
        raise DatabaseException(detail=str(e))

@router.get("/{title}", response_model=Song)
def get_song_by_title(title: str, db: Session = Depends(get_db)):
    try:
        song = db.query(SongModel).filter(SongModel.title == title).first()
        if not song:
            raise SongNotFoundException()
        return song
    except SQLAlchemyError as e:
        raise DatabaseException(detail=str(e))

@router.post("/rate_song/{song_id}", response_model=Song)
def rate_song(song_id: str, rating: RatedSong, db: Session = Depends(get_db)):
    try:
        song = db.query(SongModel).filter(SongModel.id==song_id).first()
        if not song:
            raise SongNotFoundException()
        song.rating = rating.rating
        db.add(song)
        db.commit()
        db.refresh(song)
        return song
    except SQLAlchemyError as e:
        raise DatabaseException(detail=str(e))