from fastapi import HTTPException

class SongNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Song not found")

class DatabaseException(HTTPException):
    def __init__(self, detail: str = "Database error"):
        super().__init__(status_code=500, detail=detail)
