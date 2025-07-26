from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class ClassOut(BaseModel):
    id: UUID
    name: str
    instructor: str
    start_time: datetime
    available_slots: int

class BookIn(BaseModel):
    class_id: UUID
    client_name: str = Field(min_length=1)
    client_email: EmailStr

class BookingOut(BaseModel):
    id: UUID
    class_id: UUID
    client_name: str
    client_email: EmailStr
    booked_at: datetime
    class_start_time: datetime
    class_name: str

class ErrorResp(BaseModel):
    detail: str

class ClassesResp(BaseModel):
    classes: List[ClassOut]

class BookingsResp(BaseModel):
    bookings: List[BookingOut]
