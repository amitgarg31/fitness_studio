# Fitness Booking API (FastAPI)

A simple booking API for a fitness studio (Yoga, Zumba, HIIT).  
Stores datetimes in **UTC**, seeds classes defined in **IST**, and converts to the requested timezones on read.

---

## **Stack**
- **FastAPI**
- **SQLModel + SQLite**
- **Pytest**
- **zoneinfo** for timezones

---

## **Setup**

Clone the repository and set up the environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```

---

## **API Endpoints & Examples**

### **1. List Classes**
**Endpoint:**  
`GET /classes`

**Description:**  
Returns a list of all upcoming fitness classes.

**Example cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/classes?timezone=Asia/Kolkata"   -H "accept: application/json"
```

---

### **2. Book a Class**
**Endpoint:**  
`POST /book`

**Description:**  
Books a spot for a specific class if slots are available.

**Example cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/book"   -H "Content-Type: application/json"   -d '{
    "class_id": "c0c6becf-e657-4a60-b3b3-0bcb436a88a9",
    "client_name": "Amit Sharma",
    "client_email": "as1000amit@gmail.com"
  }'
```

---

### **3. Get Bookings by Email**
**Endpoint:**  
`GET /bookings`

**Description:**  
Returns all bookings made by a specific email address.

**Example cURL:**
```bash
curl -X GET "http://127.0.0.1:8000/bookings?email=as1000amit@gmail.com&timezone=Asia/Kolkata"   -H "accept: application/json"
```

---

## **Testing**

Run the tests using `pytest`:

```bash
pytest
```

---

## **License**

This project is open source and available under the [MIT License](LICENSE).
