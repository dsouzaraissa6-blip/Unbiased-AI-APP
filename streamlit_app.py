import streamlit as st
import pandas as pd
import joblib



st.divider()

# ---------------- ACTION BUTTON ----------------
run = st.button("🔍 Run Diagnosis")

# ---------------- TOGGLE FOR COMPARISON ----------------
compare = st.toggle("🔄 Compare with other gender")

if run:

    # Prepare input
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

    # Predictions
    pred_user = model_b.predict(input_user)[0]
    pred_other = model_b.predict(input_other)[0]

    # ---------------- OUTPUT ----------------
    st.subheader("🤖 Your Diagnosis")

    if pred_user == 1:
        st.error("High Risk")
    else:
        st.success("Low Risk")

    # ---------------- COMPARISON ----------------
    if compare:
        st.subheader("🔍 Bias Check (Same data, different gender)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**You ({gender})**")
            st.write("High Risk" if pred_user == 1 else "Low Risk")

        with col2:
            other_gender = "Female" if gender == "Male" else "Male"
            st.markdown(f"**Same person but {other_gender}**")
            st.write("High Risk" if pred_other == 1 else "Low Risk")

        # Explanation
        if pred_user != pred_other:
            st.warning(
                "⚠️ Changing ONLY gender changed the prediction.\n\n"
                "➡️ This indicates bias in the model."
            )
        else:
            st.success(
                "✅ Changing gender did NOT affect prediction.\n\n"
                "➡️ No bias observed for this case."
            )
