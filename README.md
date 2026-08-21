# FastAPI Projects — Abhishek Kumar

This repository contains two independent FastAPI projects, each in its own subfolder with its own README.

## Projects

### [Patient Management API](./patient-management)
A CRUD API for managing patient records with automatic BMI calculation and categorization.
**Tech:** FastAPI, Pydantic

### [Insurance Premium Prediction API](./insurance-premium-prediction)
An ML-powered API predicting insurance premium category, with a Streamlit frontend.
**Tech:** FastAPI, Pydantic, Scikit-learn, Streamlit

## Folder Structure

Fast Api/
├── patient-management/
│ ├── main.py
│ ├── patients.json
│ └── README.md
├── insurance-premium-prediction/
│ ├── app.py
│ ├── frontend.py
│ ├── model.pkl
│ └── README.md
├── requirements.txt
├── .gitignore
└── README.md


## Setup (shared across both projects)

```bash
git clone https://github.com/akumar2022-26/Patient-Management-Api.git
cd Patient-Management-Api

python -m venv myenv
myenv\Scripts\activate      # Windows
source myenv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Then `cd` into whichever project folder you want to run — see that folder's README for run commands and endpoints.