from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List
from app.config import unique_id  

class FitnessClass(SQLModel, table=True):
    id: UUID = Field(default_factory=unique_id, primary_key=True, index=True)
    name: str
    instructor: str
    capacity: int
    booked: int = 0
    start_time_utc: datetime

    bookings: List["Booking"] = Relationship(back_populates="clazz")


class Booking(SQLModel, table=True):
    id: UUID = Field(default_factory=unique_id, primary_key=True, index=True)
    class_id: UUID = Field(foreign_key="fitnessclass.id", index=True)
    client_name: str
    client_email: str
    booked_at_utc: datetime

    clazz: FitnessClass = Relationship(back_populates="bookings")
