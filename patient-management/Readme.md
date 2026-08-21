# Patient Management API

A simple CRUD API built with FastAPI for managing patient records, with automatic BMI
calculation and categorization.

## Features
- Create, read, update, and delete patient records
- Automatic BMI and BMI category calculation (computed at read-time, not stored)
- Sort patients by any field, ascending or descending
- Input validation via Pydantic (height/weight must be positive, gender restricted to Male/Female)
- JSON file storage (`patients.json`) — no database setup required

## Tech Stack
- FastAPI
- Pydantic v2 (computed fields, `Annotated` field metadata)
- Uvicorn (ASGI server)

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/akumar2022-26/Patient-Management-Api.git
cd Patient-Management-Api/patient-management
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv myenv
myenv\Scripts\activate      # Windows
source myenv/bin/activate   # macOS/Linux

pip install -r ../requirements.txt
```

### 3. Run the server
```bash
uvicorn main:app --reload
```
API at `http://127.0.0.1:8000`, Swagger docs at `http://127.0.0.1:8000/docs`.

## API Endpoints

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

### Example: Add a patient
```bash
curl -X POST http://127.0.0.1:8000/add \
  -H "Content-Type: application/json" \
  -d '{"id":"P006","name":"John Doe","city":"NYC","age":30,"gender":"Male","height":180,"weight":75}'
```

## Notes
- `bmi` and `bmi_category` are computed on the fly from height/weight and are **not** persisted
  to `patients.json` — only the raw patient fields are stored.
- Data is stored in a flat JSON file for simplicity; swap `load_data`/`save_data` for a real
  database (e.g. PostgreSQL + SQLAlchemy) for production use.