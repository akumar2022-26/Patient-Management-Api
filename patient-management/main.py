from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated,Literal,Optional
class Patient(BaseModel):
    id: Annotated[str, Field(...,description="The ID of the patient")]
    name: Annotated[str, Field(...,description="The name of the patient")]
    city: Annotated[str, Field(...,description="The city of the patient")]
    age: Annotated[int, Field(...,description="The age of the patient")]
    gender: Annotated[str, Literal["Male", "Female"], Field(...,description="The gender of the patient")]
    height: Annotated[float, Field(...,gt=0,description="The height of the patient")]
    weight: Annotated[float, Field(...,gt=0,description="The weight of the patient")]
    @computed_field(description="The BMI of the patient")
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    @computed_field(description="The BMI category of the patient")
    @property
    def bmi_category(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None,description="The name of the patient")]
    city: Annotated[Optional[str], Field(None,description="The city of the patient")]
    age: Annotated[Optional[int], Field(None,description="The age of the patient")]
    gender: Annotated[Optional[str], Literal["Male", "Female"], Field(None,description="The gender of the patient")]
    height: Annotated[Optional[float], Field(None,gt=0,description="The height of the patient")]
    weight: Annotated[Optional[float], Field(None,gt=0,description="The weight of the patient")]
    
app = FastAPI()
def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)
@app.get("/")
def read_root():
    return {"message":"Welcome to the Patient Management System API!"}
@app.get('/about')
def about():
    return {"message": "Fully functional Patient Management System API"}
@app.get('/view')
def view_patients():
    data = load_data()
    return data
@app.get('/patient/{id}')
def view_patient(id: str=Path(...,description="The ID of the patient to retrieve",examples=["PTT1082"])):
    data = load_data()
    for patient in data:
        if patient.get("id") == id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")
@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description="The field to sort by", examples=["age"]),
    order: str = Query("asc", description="Sort direction: asc or desc", examples=["asc"])
):
    data = load_data()
    valid_fields = ["id", "name", "city", "age", "gender", "height", "weight"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail=f"Invalid order: {order}")
    sorted_data = sorted(data, key=lambda x: x.get(sort_by, 0), reverse=order == "desc")
    return sorted_data
@app.post('/add')
def create_patient(patient:Patient):
    # load existing data
    data = load_data()

    #check if the patient already exists
    if any(existing_patient.get("id") == patient.id for existing_patient in data):
        raise HTTPException(status_code=400,detail='patient already exists')

    #new patient add to the database
    data.append(patient.model_dump(exclude={"bmi", "bmi_category"}))

    #save into the data
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'Response created'})
@app.put('/update/{id}')
def update_patient(id:str,patient_update:PatientUpdate):
    data = load_data()
    existing_patient_info = next(
        (patient for patient in data if patient.get("id") == id),
        None,
    )
    if existing_patient_info is None:
        raise HTTPException(status_code=404, detail='Patient Not Found')
    update_patient_info=patient_update.model_dump(exclude_unset=True)
    for key,value in update_patient_info.items():
        existing_patient_info[key]=value

    existing_patient_info["id"] = id
    patient_pydantic_object=Patient(**existing_patient_info)
    updated_patient_info = patient_pydantic_object.model_dump(exclude={"bmi", "bmi_category"})
    patient_index = data.index(existing_patient_info)
    data[patient_index] = updated_patient_info
    # save the updated data back to the JSON file
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'Patient updated successfully'})
@app.delete('/delete/{id}')
def delete_patient(id:str):
    data = load_data()
    patient_to_delete = next(
        (patient for patient in data if patient.get("id") == id),
        None,
    )
    if patient_to_delete is None:
        raise HTTPException(status_code=404, detail='Patient Not Found')
    data.remove(patient_to_delete)
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'Patient deleted successfully'})