import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions import DatabaseException, SongNotFoundException
from src.models import Song as SongModel
from src.routers.playlist import get_songs

@pytest.fixture
def db_session():
    # Create a mock database session for testing
    db = Session()
    yield db
    db.close()

@pytest.fixture
def mock_db_query(mocker):
    # Mock the database query method
    query_mock = mocker.patch('sqlalchemy.orm.Session.query')
    yield query_mock

def test_get_songs_with_songs(db_session, mock_db_query):
    # Set up the mock database query to return some songs
    mock_db_query.return_value.offset.return_value.limit.return_value.all.return_value = [SongModel(), SongModel()]

    # Call the function
    songs = get_songs(page=1, per_page=10, db=db_session)

    # Assert that the correct songs are returned
    assert len(songs) == 2
    assert isinstance(songs[0], SongModel)
    assert isinstance(songs[1], SongModel)

def test_get_songs_without_songs(db_session, mock_db_query):
    # Set up the mock database query to return no songs
    mock_db_query.return_value.offset.return_value.limit.return_value.all.return_value = []

    # Assert that a SongNotFoundException is raised
    with pytest.raises(SongNotFoundException):
        get_songs(page=1, per_page=10, db=db_session)

def test_get_songs_with_database_error(db_session, mock_db_query):
    # Set up the mock database query to raise an error
    mock_db_query.side_effect = SQLAlchemyError("Database error")

    # Assert that a DatabaseException is raised
    with pytest.raises(DatabaseException):
        get_songs(page=1, per_page=10, db=db_session)
