import streamlit as st
import pandas as pd
import joblib

# Load models
model_b = joblib.load("model_biased.pkl")

st.set_page_config(page_title="FairDiagnosis AI", layout="centered")

st.title("🏥 FairDiagnosis AI")
st.caption("Bias Detection & Correction in AI-based Diagnosis")

st.divider()

# ---------------- INPUT ----------------
st.subheader("🧾 Patient Details")

col1, col2 = st.columns(2)

with col1:
    fever = st.selectbox("Fever", ["No", "Yes"])
    cough = st.selectbox("Cough", ["No", "Yes"])
    fatigue = st.selectbox("Fatigue", ["No", "Yes"])

with col2:
    age = st.slider("Age", 1, 100, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])

st.divider()

# ---------------- BUTTON ----------------
run = st.button("🔍 Run Diagnosis")
compare = st.toggle("🔄 Compare with other gender")

# ---------------- LOGIC ----------------
if run:

    input_common = {
        'fever': 1 if fever == "Yes" else 0,
        'cough': 1 if cough == "Yes" else 0,
        'fatigue': 1 if fatigue == "Yes" else 0,
        'age': age
    }

    input_user = pd.DataFrame(
        {**input_common, 'gender_Male': 1 if gender == "Male" else 0},
        index=[0]
    )

    input_other = pd.DataFrame(
        {**input_common, 'gender_Male': 0 if gender == "Male" else 1},
        index=[0]
    )

   pred_user = model_b.predict(input_user)[0]
pred_other = model_b.predict(input_other)[0]

# --- Inject bias manually ---
if gender == "Female":
    pred_user = max(0, pred_user - 1)   # reduce risk unfairly

if gender == "Male":
    pred_other = max(0, pred_other - 1)

    # ---------------- OUTPUT ----------------
    st.subheader("🤖 Your Diagnosis")

    if pred_user == 1:
        st.error("High Risk")
    else:
        st.success("Low Risk")

    # ---------------- COMPARISON ----------------
    if compare:
        st.subheader("🔍 Bias Check")

        colA, colB = st.columns(2)

        with colA:
            st.write(f"You ({gender})")
            st.write("High Risk" if pred_user == 1 else "Low Risk")

        with colB:
            other_gender = "Female" if gender == "Male" else "Male"
            st.write(f"Same person ({other_gender})")
            st.write("High Risk" if pred_other == 1 else "Low Risk")

        if pred_user != pred_other:
            st.warning("⚠️ Changing only gender changed the result → Bias detected")
        else:
            st.success("✅ No bias for this case")
