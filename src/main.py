from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager

from src.routers import playlist
from src.database import engine, Base
from src.one_timer import load_json_to_db
from src.exceptions import SongNotFoundException
from src.exception_handlers import song_not_found_exception_handler
from src.exception_handlers import database_exception_handler

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(playlist.router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    load_json_to_db()
    yield
    # Shutdown code (if needed)
    print("Shutting down...")

app.router.lifespan_context = lifespan

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI project!"}

app.add_exception_handler(SongNotFoundException, song_not_found_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
