from datetime import datetime, timedelta
from sqlmodel import Session,select
from app.db import engine, init_db
from app.models import FitnessClass
from app.timezone import ist_to_utc
from zoneinfo import ZoneInfo

def run():
    init_db()
    with Session(engine) as session:
        if session.exec(select(FitnessClass).limit(1)).first():
            return
        now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
        data = [
            ("Yoga", "Aarti", now_ist + timedelta(days=1, hours=7), 20),
            ("Zumba", "Neeraj", now_ist + timedelta(days=1, hours=9), 15),
            ("HIIT", "Sam",   now_ist + timedelta(days=2, hours=6), 10),
        ]
        for name, instructor, start_ist, cap in data:
            session.add(FitnessClass(
                name=name,
                instructor=instructor,
                capacity=cap,
                start_time_utc=ist_to_utc(start_ist)
            ))
        session.commit()

if __name__ == "__main__":
    run()
