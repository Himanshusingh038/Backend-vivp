import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from src.exceptions import DatabaseException, SongNotFoundException
from src.models import Song as SongModel
from src.routers.playlist import rate_song
from src.schemas.rate_song_schema import RatedSong

@pytest.fixture
def db_session(mocker):
    # Create a mock database session for testing
    db = mocker.Mock(spec=Session)
    yield db

def test_rate_song_valid(db_session, mocker):
    # Set up the mock database query to return a song
    mocker.patch('src.routers.playlist.get_db', return_value=db_session)
    mock_query = mocker.patch.object(db_session, 'query')
    mock_filter = mock_query.return_value.filter
    mock_filter.return_value.first.return_value = SongModel(id="1", title="Test Song", rating=0)

    # Call the function
    song = rate_song(song_id="1", rating=RatedSong(rating=5), db=db_session)

    # Assert that the song has been rated correctly
    assert song.rating == 5

def test_rate_song_not_found(db_session, mocker):
    # Set up the mock database query to return None
    mocker.patch('src.routers.playlist.get_db', return_value=db_session)
    mock_query = mocker.patch.object(db_session, 'query')
    mock_filter = mock_query.return_value.filter
    mock_filter.return_value.first.return_value = None

    # Assert that a SongNotFoundException is raised
    with pytest.raises(SongNotFoundException):
        rate_song(song_id="1", rating=RatedSong(rating=5), db=db_session)

def test_rate_song_invalid_rating(db_session, mocker):
    # Set up the mock database query to return a song
    mocker.patch('src.routers.playlist.get_db', return_value=db_session)
    mock_query = mocker.patch.object(db_session, 'query')
    mock_filter = mock_query.return_value.filter
    mock_filter.return_value.first.return_value = SongModel(id="1", title="Test Song", rating=0)

    # Assert that a ValidationError is raised
    with pytest.raises(ValidationError):
        rate_song(song_id="1", rating=RatedSong(rating=6), db=db_session)

def test_rate_song_database_error(db_session, mocker):
    # Set up the mock database query to raise an error
    mocker.patch('src.routers.playlist.get_db', return_value=db_session)
    mock_query = mocker.patch.object(db_session, 'query')
    mock_filter = mock_query.return_value.filter
    mock_filter.return_value.first.side_effect = SQLAlchemyError("Database error")

    # Assert that a DatabaseException is raised
    with pytest.raises(DatabaseException):
        rate_song(song_id="1", rating=RatedSong(rating=5), db=db_session)
