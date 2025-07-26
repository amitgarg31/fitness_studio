Fitness Booking API
This is a simple API for booking fitness classes like Yoga, Zumba, and HIIT. It helps you manage class schedules and client bookings for a fitness studio.

✨ Features
Class Scheduling: Define and manage various fitness classes.

Timezone Handling: Stores all class times in UTC and converts them to your preferred timezone when you view them.

Booking System: Allows clients to book available slots in classes.

Booking Management: Easily retrieve all bookings made by a specific client.

🚀 Tech Stack
FastAPI: A modern, fast web framework for building APIs with Python.

SQLModel: A library for interacting with SQL databases using Python objects (built on top of SQLAlchemy and Pydantic).

SQLite: A lightweight, file-based database.

Pytest: A testing framework for Python.

zoneinfo: For accurate timezone conversions.

⚙️ Setup
Follow these steps to get the project running on your local machine:

Clone the repository (if applicable, or assume the user has the files).

Create a virtual environment:

python -m venv .venv

Activate the virtual environment:

Windows:

.venv\Scripts\activate

macOS/Linux:

source .venv/bin/activate

Install dependencies:
Create a requirements.txt file in your project root with the following content:

fastapi
uvicorn[standard]
sqlmodel
pytest
python-multipart
python-dotenv
tzdata # For zoneinfo

Then install them:

pip install -r requirements.txt

📊 Seed Initial Data
Run this command to populate your database with some initial fitness classes (defined in IST):

python -m app.seed

🏃‍♀️ Running the Application
Start the API server using Uvicorn:

uvicorn app.main:app --reload

The API will be available at http://127.0.0.1:8000.

🧪 Testing
Run tests using Pytest:

pytest

🌐 API Endpoints
Here are the main API endpoints and how to use them:

1. List Classes
Get a list of all upcoming fitness classes. You can specify a timezone to see class times in your local time.

Endpoint: GET /classes

Example (showing times in Asia/Kolkata):

curl -X GET "http://127.0.0.1:8000/classes?timezone=Asia/Kolkata" \
-H "accept: application/json"

2. Book a Class
Book a spot in a specific class. Make sure the class_id is correct and slots are available.

Endpoint: POST /book

Example:

curl -X POST "http://127.0.0.1:8000/book" \
-H "Content-Type: application/json" \
-d '{
  "class_id": "c0c6becf-e657-4a60-b3b3-0bcb436a88a9",
  "client_name": "Amit Sharma",
  "client_email": "as1000amit@gmail.com"
}'

(Note: Replace c0c6becf-e657-4a60-b3b3-0bcb436a88a9 with an actual class ID from the /classes endpoint.)

3. Get Bookings by Email
Retrieve all bookings made by a specific email address. You can also specify a timezone for the booking times.

Endpoint: GET /bookings

Example (showing times in Asia/Kolkata):

curl -X GET "http://127.0.0.1:8000/bookings?email=as1000amit@gmail.com&timezone=Asia/Kolkata" \
-H "accept: application/json"
