# Insurance Premium Prediction API

An ML-powered API that predicts insurance premium category (Low/Medium/High) based on user
details, built with FastAPI and served through a Streamlit frontend.

## Features
- REST API built with FastAPI, validated using Pydantic
- Feature engineering via Pydantic computed fields (BMI, lifestyle risk, age group, city tier)
- Trained scikit-learn classification pipeline (serialized with pickle)
- Streamlit frontend for interactive predictions

## Tech Stack
- FastAPI, Pydantic v2
- Scikit-learn, Pandas
- Streamlit
- Uvicorn

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/akumar2022-26/Patient-Management-Api.git
cd Patient-Management-Api/insurance-premium-prediction
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv myenv
myenv\Scripts\activate      # Windows
source myenv/bin/activate   # macOS/Linux

pip install -r ../requirements.txt
```

### 3. Run the backend
```bash
uvicorn app:app --reload
```
API at `http://127.0.0.1:8000`, Swagger docs at `http://127.0.0.1:8000/docs`.

### 4. Run the frontend
```bash
streamlit run frontend.py
```

## API Endpoint

| Method | Endpoint    | Description                          |
|--------|-------------|---------------------------------------|
| POST   | `/predict`  | Predicts insurance premium category   |

### Example request
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age":29,"weight":70,"height":1.78,"income_lpa":5,"smoker":true,"city":"Mumbai","occupation":"retired"}'
```

## Notes
- Category mapping (`0/1/2` → Low/Medium/High) is derived from the model's training label encoding.
- `model.pkl` contains the trained scikit-learn pipeline used for inference.