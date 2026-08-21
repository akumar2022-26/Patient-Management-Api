# FastAPI Projects — Abhishek Kumar

This repository contains two FastAPI-based projects:

1. [Patient Management API](#1-patient-management-api) — a CRUD API for managing patient records
2. [Insurance Premium Prediction API](#2-insurance-premium-prediction-api) — an ML-powered API that predicts insurance premium category

---

## 1. Patient Management API

A simple CRUD API built with FastAPI for managing patient records, with automatic BMI
calculation and categorization.

### Features
- Create, read, update, and delete patient records
- Automatic BMI and BMI category calculation (computed at read-time, not stored)
- Sort patients by any field, ascending or descending
- Input validation via Pydantic (height/weight must be positive, gender restricted to Male/Female)
- JSON file storage (`patients.json`) — no database setup required

### Run it
```bash
uvicorn main:app --reload
```
API at `http://127.0.0.1:8000`, Swagger docs at `http://127.0.0.1:8000/docs`.

### Endpoints

| Method | Endpoint          | Description                          |
|--------|-------------------|---------------------------------------|
| GET    | `/`                | Welcome message                       |
| GET    | `/about`           | API description                       |
| GET    | `/view`            | List all patients                     |
| GET    | `/patient/{id}`    | Get a single patient by ID            |
| GET    | `/sort`            | Sort patients by field and order      |
| POST   | `/add`             | Add a new patient                     |
| PUT    | `/update/{id}`     | Update an existing patient            |
| DELETE | `/delete/{id}`     | Delete a patient                      |

### Example
```bash
curl -X POST http://127.0.0.1:8000/add \
  -H "Content-Type: application/json" \
  -d '{"id":"P006","name":"John Doe","city":"NYC","age":30,"gender":"Male","height":180,"weight":75}'
```

---

## 2. Insurance Premium Prediction API

An ML-powered API that predicts insurance premium category (Low/Medium/High) based on user
details, built with FastAPI and served through a Streamlit frontend.

### Features
- REST API built with FastAPI, validated using Pydantic
- Feature engineering via Pydantic computed fields (BMI, lifestyle risk, age group, city tier)
- Trained scikit-learn classification pipeline (serialized with pickle)
- Streamlit frontend for interactive predictions

### Run the backend
```bash
uvicorn app:app --reload
```
API at `http://127.0.0.1:8000`, Swagger docs at `http://127.0.0.1:8000/docs`.

### Run the frontend
```bash
streamlit run frontend.py
```

### Endpoint

| Method | Endpoint    | Description                          |
|--------|-------------|---------------------------------------|
| POST   | `/predict`  | Predicts insurance premium category   |

### Example
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age":29,"weight":70,"height":1.78,"income_lpa":5,"smoker":true,"city":"Mumbai","occupation":"retired"}'
```

---

## Tech Stack

- FastAPI, Pydantic v2 (computed fields, `Annotated` field metadata)
- Scikit-learn, Pandas
- Streamlit
- Uvicorn (ASGI server)

## Getting Started (both projects)

### 1. Clone the repo
```bash
git clone https://github.com/akumar2022-26/Patient-Management-Api.git
cd Patient-Management-Api
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv myenv
myenv\Scripts\activate      # Windows
source myenv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### 3. Run whichever project you want (see run commands above)

## Notes

- Patient Management API: `bmi` and `bmi_category` are computed on the fly and not persisted to `patients.json`.
- Insurance Premium Prediction API: category mapping (`0/1/2` → Low/Medium/High) is derived from the model's training label encoding.