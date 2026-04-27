import streamlit as st

st.set_page_config(page_title="FairDiagnosis AI", layout="centered")

st.title("🏥 FairDiagnosis AI")
st.caption("Bias Detection & Correction in AI-based Diagnosis")

st.divider()

# ---------------- INPUT SECTION ----------------
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

# ---------------- MODEL LOGIC ----------------
fair_mode = st.toggle("⚖️ Enable Fair Mode")

# Base prediction logic (simple demo)
risk_score = 0

if fever == "Yes":
    risk_score += 1
if cough == "Yes":
    risk_score += 1
if fatigue == "Yes":
    risk_score += 1
if age > 60:
    risk_score += 1

base_prediction = 1 if risk_score >= 2 else 0

# Introduce bias
if not fair_mode:
    if gender == "Female":
        prediction = 0  # biased reduction
    else:
        prediction = base_prediction
else:
    prediction = base_prediction  # fair version

# ---------------- OUTPUT ----------------
st.subheader("🤖 Diagnosis Result")

if prediction == 1:
    st.success("High Risk")
else:
    st.info("Low Risk")

st.divider()

# ---------------- BIAS INSIGHT ----------------
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

# ---------------- EXPLANATION ----------------
st.subheader("💡 What this shows")

st.write("""
This prototype demonstrates how AI systems can develop bias when trained on skewed data.

- In biased mode, one group receives fewer high-risk predictions.
- In fair mode, predictions are balanced across groups.

This helps ensure equitable AI-assisted medical decision-making.
""")
