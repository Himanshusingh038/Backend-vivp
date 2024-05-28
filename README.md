# FastAPI Template Project

This is a template project for FastAPI with a basic setup including a router, database, and models.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Databases
- Alembic
- Python-dotenv

## Setup

1. Clone the repository
2. Create a virtual environment and activate it
3. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Create a `.env` file and set your `DATABASE_URL`:
    ```
    DATABASE_URL=sqlite:///./test.db
    ```
5. Initialize the database with Alembic:
    ```
    alembic init alembic
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
    ```
6. Run the application:
    ```
    uvicorn app.main:app --reload
    ```

## Endpoints

- GET `/` - Root endpoint
- POST `/items/` - Create a new item
- GET `/items/{item_id}` - Get an item by ID
