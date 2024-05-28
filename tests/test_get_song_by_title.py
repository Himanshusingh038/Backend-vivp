import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions import DatabaseException, SongNotFoundException
from src.models import Song as SongModel
from src.routers.playlist import get_song_by_title

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

@pytest.mark.asyncio
def test_get_song_by_title_with_existing_title(db_session, mock_db_query):
    # Set up the mock database query to return a song
    mock_db_query.return_value.filter.return_value.first.return_value = SongModel(title="Test Song")

    # Call the function
    song = get_song_by_title("Test Song", db=db_session)

    # Assert that the correct song is returned
    assert song.title == "Test Song"
    
@pytest.mark.asyncio
async def test_get_song_by_title_with_non_existing_title(db_session, mock_db_query):
    # Set up the mock database query to return None
    mock_db_query.return_value.filter.return_value.first.return_value = None

    # Assert that a SongNotFoundException is raised
    with pytest.raises(SongNotFoundException):
        await get_song_by_title("Non Existing Title", db=db_session)

@pytest.mark.asyncio
async def test_get_song_by_title_with_database_error(db_session, mock_db_query):
    # Set up the mock database query to raise an error
    mock_db_query.side_effect = SQLAlchemyError("Database error")

    # Assert that a DatabaseException is raised
    with pytest.raises(DatabaseException):
        await get_song_by_title("Test Song", db=db_session)
