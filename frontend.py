import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"
st.title("Insurance Premium Prediction")
st.markdown("Enter your details below")

# Input Fields
age = st.number_input("Age", min_value=1, max_value=120, value=25)
weight = st.number_input("Weight (in kg)", min_value=1.0, value=70.0)
height = st.number_input("Height (in meters)", min_value=0.1, max_value=10.0, value=1.75)
income_lpa = st.number_input("Annual Salary (in LPA)", min_value=0.0, value=5.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City",value="Mumbai")
occupation = st.selectbox("Occupation", options=['retired', 'employed', 'unemployed', 'student', 'freelancer', 'private_job','government_job'])

if st.button("Predict Premium Category"):
    data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Premium Category: {result['predicted_category']}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.RequestException.ConnectionError:
        st.error("Failed to connect to the API. Please ensure the backend is running.")