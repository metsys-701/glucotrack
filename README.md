# 🩺 Diabetes Tracking API

## 📌 Overview

Diabetes Tracking API is a backend application designed to manage and monitor glucose measurements and insulin usage.

The API allows users to:
- Create glucose measurement records
- Update existing records
- Retrieve stored data
- Manage insulin usage entries

This project was developed as a backend practice project focusing on RESTful API design, clean architecture, and data validation.

---

## 🚀 Technologies Used

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn

---

## 📂 Project Structure

```
├── app/                   # Main application source code
├── test_glucose.json      # Sample request payload
├── test_update.json       # Sample update payload
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Create Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

API will run at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

---

## 🧪 Example Request Payload

### Create Glucose Record

```json
{
  "date": "2026-01-31",
  "time": "08:30:00",
  "meal_type": "breakfast",
  "fasting_glucose": 110,
  "postprandial_glucose": 145,
  "insulin_units": 4.5,
  "notes": "Normal morning measurement"
}
```

### Update Glucose Record

```json
{
  "fasting_glucose": 115,
  "notes": "Updated value"
}
```

---

## 🔐 Security Notes

- No real patient data is included in this repository.
- Environment variables are excluded using `.gitignore`.
- Sensitive configuration values should be stored securely in a `.env` file.

---

## 🎯 Future Improvements

- User authentication (JWT)
- Role-based authorization
- Docker support
- PostgreSQL integration
- Unit and integration tests
- Basic analytics dashboard

---

## 📄 License

This project was created for educational and portfolio purposes.
