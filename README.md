# FastAPI Template Project

This is a template project for FastAPI with a basic setup including a router, database, and models.

## Requirements

- fastapi
- uvicorn
- sqlalchemy
- pydantic
- databases
- alembic
- python-dotenv
- pandas
- pytest
- httpx
- pytest-mock

## Setup

1. Clone the repository
2. Create a virtual env
```
python3 -m venv venv
```
3. Activate 
```
source venv/bin/activate
```
4. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```
5. Create a `.env` file and set your `DATABASE_URL`:
    ```
    DATABASE_URL=sqlite:///./playlist-db.db
    ```
6. Initialize the database with Alembic to create migration:
    ```
    alembic upgrade head
    ```
7. Run the application:
    ```
    uvicorn src.main:app --reload
    ```

## Endpoints
Open the link
 ```
http://127.0.0.1:8000/docs
 ```
- GET `/` - Root endpoint
- GET `/songs/get_songs` - Get the list of songs json body
- GET `/songs/{title}` - Get an song by Title
- POST `/songs/rate_song/{song_id}` in the body {"rating": 4} send it and the song ewill be rated

