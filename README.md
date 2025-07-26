# Fitness Booking API (FastAPI)

A simple booking API for a fitness studio (Yoga, Zumba, HIIT). Stores datetimes in UTC, seeds classes defined in IST, and converts to requested timezones on read.

## Stack
- FastAPI
- SQLModel + SQLite
- Pytest
- zoneinfo for timezones

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
