import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import Session, select

from app.db import init_db, get_session
from app.models import FitnessClass, Booking
from app.schemas import (
    ClassesResp, ClassOut, BookIn, BookingOut, BookingsResp, ErrorResp
)
from app.timezone import utc_to_tz
from app.config import settings

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Fitness Booking API", version="1.0.0", lifespan=lifespan)


@app.get("/classes", response_model=ClassesResp, responses={400: {"model": ErrorResp}})
def list_classes(
    timezone: str = Query(default=settings.default_tz),
    session: Session = Depends(get_session),
):
    try:
        ZoneInfo(timezone)
    except Exception:
        raise HTTPException(400, detail="Invalid timezone")

    fitness_classes = session.exec(
        select(FitnessClass).order_by(FitnessClass.start_time_utc)
    ).all()

    classes_out: list[ClassOut] = []
    for fitness_class in fitness_classes:
        classes_out.append(
            ClassOut(
                id=fitness_class.id,
                name=fitness_class.name,
                instructor=fitness_class.instructor,
                start_time=utc_to_tz(fitness_class.start_time_utc, timezone),
                available_slots=fitness_class.capacity - fitness_class.booked,
            )
        )
    return ClassesResp(classes=classes_out)


@app.post("/book", response_model=BookingOut, responses={400: {"model": ErrorResp}, 404: {"model": ErrorResp}})
def book(
    booking_request: BookIn,
    session: Session = Depends(get_session),
):
    fitness_class = session.get(FitnessClass, booking_request.class_id)
    if not fitness_class:
        raise HTTPException(404, detail="Class not found")

    if fitness_class.booked >= fitness_class.capacity:
        raise HTTPException(400, detail="No slots available")

    booking_record = Booking(
        class_id=fitness_class.id,
        client_name=booking_request.client_name,
        client_email=booking_request.client_email,
        booked_at_utc=datetime.utcnow(),
    )

    fitness_class.booked += 1
    session.add(booking_record)
    session.add(fitness_class)
    session.commit()
    session.refresh(booking_record)

    return BookingOut(
        id=booking_record.id,
        class_id=booking_record.class_id,
        client_name=booking_record.client_name,
        client_email=booking_record.client_email,
        booked_at=booking_record.booked_at_utc.replace(tzinfo=ZoneInfo("UTC")),
        class_start_time=fitness_class.start_time_utc.replace(tzinfo=ZoneInfo("UTC")),
        class_name=fitness_class.name,
    )


@app.get("/bookings", response_model=BookingsResp, responses={400: {"model": ErrorResp}})
def bookings(
    email: str = Query(..., description="Client email"),
    timezone: str = Query(default=settings.default_tz),
    session: Session = Depends(get_session),
):
    try:
        ZoneInfo(timezone)
    except Exception:
        raise HTTPException(400, detail="Invalid timezone")

    query = (
        select(Booking, FitnessClass)
        .join(FitnessClass, FitnessClass.id == Booking.class_id)
        .where(Booking.client_email == email)
        .order_by(Booking.booked_at_utc.desc())
    )
    results = session.exec(query).all()

    bookings_out: list[BookingOut] = []
    for booking_record, fitness_class in results:
        bookings_out.append(
            BookingOut(
                id=booking_record.id,
                class_id=fitness_class.id,
                client_name=booking_record.client_name,
                client_email=booking_record.client_email,
                booked_at=utc_to_tz(booking_record.booked_at_utc, timezone),
                class_start_time=utc_to_tz(fitness_class.start_time_utc, timezone),
                class_name=fitness_class.name,
            )
        )

    return BookingsResp(bookings=bookings_out)
