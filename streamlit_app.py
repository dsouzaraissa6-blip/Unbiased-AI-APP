import streamlit as st
import pandas as pd

st.title("FairDiagnosis AI")

st.write("Demo: Bias detection and correction in diagnosis")

# Fake inputs (simple for demo)
fever = st.selectbox("Fever", ["Yes", "No"])
cough = st.selectbox("Cough", ["Yes", "No"])
gender = st.selectbox("Gender", ["Male", "Female"])

fair_mode = st.toggle("Fair Mode")

# Simple mock prediction logic (replace with your idea)
if fever == "Yes" and cough == "Yes":
    base_prediction = 1
else:
    base_prediction = 0

# Introduce bias
if not fair_mode:
    if gender == "Male":
        prediction = base_prediction
    else:
        prediction = 0  # biased against females
else:
    prediction = base_prediction  # fair version

# Output
st.subheader("Prediction")
if prediction == 1:
    st.write("High Risk")
else:
    st.write("Low Risk")

# Bias display
st.subheader("Bias Insight")

st.write("Before Fix: Female lower predictions than Male")
st.write("After Fix: Balanced predictions across groups")