from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated,Literal,Optional
import pickle
import pandas as pd

# Load the model from the pickle file
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()
tier_1_cities=[
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad"
  ]
tier_2_cities=[
    "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore",
    "Bhopal", "Visakhapatnam", "Patna", "Vadodara", "Ludhiana",
    "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot",
    "Varanasi", "Srinagar", "Amritsar", "Jodhpur", "Coimbatore",
    "Guwahati", "Chandigarh", "Mysore", "Jalandhar"
  ]

# pydantic model to validate the incoming data
class UserInput(BaseModel):
    age: Annotated[int,Field(..., gt=0, lt=120, description='Age of the user')]
    weight: Annotated[float,Field(..., gt=0, description='Weight of the user')]
    height: Annotated[float,Field(..., gt=0, lt=10, description='Height of the user')]
    income_lpa: Annotated[float,Field(..., gt=0, description='Annual salary of the user')]
    smoker: Annotated[bool,Field(..., description='Is user a smoker')]
    city: Annotated[str,Field(..., description='The city that user to the belong')]
    occupation: Annotated[Literal['retired', 'employed', 'unemployed', 'student', 'freelancer', 'private_job','government_job'],Field(..., description='Occupation of the user')]
    @computed_field(description="The BMI of the user")
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 25:
            return "medium"
        else:
            return "low"
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return 'Young'
        elif self.age < 40:
            return 'Middle'
        else:
            return 'Old'
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
category_map = {0: "High", 1: "Low", 2: "Medium"}
@app.post("/predict")
def predict_prenium(data: UserInput):
    input_df = pd.DataFrame([{
            'bmi': data.bmi,
            'age_group': data.age_group,
            'city_tier': data.city_tier,
            'lifestyle_risk': data.lifestyle_risk,
            'income_lpa': data.income_lpa,
            'occupation': data.occupation
        }])

    prediction = model.predict(input_df)[0]
    predicted_category = category_map[int(prediction)]
    return JSONResponse(status_code=200, content={"predicted_category": predicted_category})
    



        

