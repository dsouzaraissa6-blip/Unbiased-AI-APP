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

# ---------------- MODEL INPUT ----------------
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

col_out1, col_out2 = st.columns(2)

with col_out1:
    st.markdown("### 🔴 Biased Model")
    if pred_b == 1:
        st.error("High Risk")
    else:
        st.success("Low Risk")

with col_out2:
    st.markdown("### 🟢 Fair Model")
    if pred_f == 1:
        st.error("High Risk")
    else:
        st.success("Low Risk")

st.divider()

# ---------------- EXPLANATION ----------------
st.subheader("💡 Explanation")

if pred_b != pred_f:
    st.warning(
        "⚠️ The prediction changed when gender was removed.\n\n"
        "This indicates the model was influenced by gender, showing bias."
    )
else:
    st.success(
        "✅ Both models gave the same result.\n\n"
        "This means gender did not affect the decision in this case."
    )

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

# ---------------- FINAL NOTE ----------------
st.subheader("🧠 What this shows")

st.write("""
This prototype demonstrates how AI systems can produce biased outcomes when sensitive features like gender are used.

- The **biased model** uses gender and may produce unfair results.
- The **fair model** removes gender to ensure more equitable decisions.

This approach helps improve fairness in AI-assisted healthcare systems.
""")
