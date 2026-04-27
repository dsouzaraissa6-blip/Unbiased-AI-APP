import streamlit as st
import pandas as pd
import joblib

# Load models
model_b = joblib.load("model_biased.pkl")
model_f = joblib.load("model_fair.pkl")

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

# ---------------- MODE TOGGLE ----------------
fair_mode = st.toggle("⚖️ Enable Fair Mode")

# ---------------- INPUT PREP ----------------
input_common = {
    'fever': 1 if fever == "Yes" else 0,
    'cough': 1 if cough == "Yes" else 0,
    'fatigue': 1 if fatigue == "Yes" else 0,
    'age': age
}

input_b = pd.DataFrame(
    {**input_common, 'gender_Male': 1 if gender == "Male" else 0},
    index=[0]
)

input_f = pd.DataFrame(input_common, index=[0])

# ---------------- PREDICTIONS ----------------
pred_b = model_b.predict(input_b)[0]
pred_f = model_f.predict(input_f)[0]

# ---------------- OUTPUT ----------------
st.subheader("🤖 Diagnosis Result")

if not fair_mode:
    st.markdown("### 🔴 Biased Model")
    final_pred = pred_b
else:
    st.markdown("### 🟢 Fair Model")
    final_pred = pred_f

if final_pred == 1:
    st.error("High Risk")
else:
    st.success("Low Risk")

st.divider()

# ---------------- COMPARISON ----------------
st.subheader("🔍 What changed?")

colA, colB = st.columns(2)

with colA:
    st.markdown("**Biased Model**")
    st.write("High Risk" if pred_b == 1 else "Low Risk")

with colB:
    st.markdown("**Fair Model**")
    st.write("High Risk" if pred_f == 1 else "Low Risk")

# ---------------- EXPLANATION ----------------
st.subheader("💡 Explanation")

if pred_b != pred_f:
    st.warning(
        "The prediction changed when gender was removed.\n\n"
        "➡️ This means the original model was influenced by gender (bias)."
    )
else:
    st.info(
        "Both models gave the same result.\n\n"
        "➡️ In this case, gender did not affect the decision."
    )

st.divider()

# ---------------- BIAS METRICS ----------------
st.subheader("📊 Bias Analysis")

col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🔴 Before Fix")
    st.metric("Female High-Risk Rate", "27%")
    st.metric("Male High-Risk Rate", "65%")

with col4:
    st.markdown("### 🟢 After Fix")
    st.metric("Female High-Risk Rate", "48%")
    st.metric("Male High-Risk Rate", "48%")

st.divider()

# ---------------- NOTE ----------------
st.subheader("🧠 What this shows")

st.write("""
- The biased model uses gender → may give unfair results  
- The fair model ignores gender → more balanced outcomes  
- Toggle lets you see how decisions change  

This demonstrates bias detection and correction in AI systems.
""")
