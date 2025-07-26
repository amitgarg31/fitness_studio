from pydantic import BaseModel
from typing import Literal
from uuid import uuid4

class Settings(BaseModel):
    db_url: str = "sqlite:///./booking.db"  # use "sqlite:///:memory:" for in-memory
    default_tz: str = "Asia/Kolkata"

settings = Settings()

def unique_id() :
    return uuid4()