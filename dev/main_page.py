import streamlit as st
import pandas as pd
import os
import joblib

current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "lr_salary_model.pkl")

st.set_page_config(page_title="Employee Salary Estimates", layout="centered")
st.title("Employee Salary Prediction System")
st.write("Enter employee parameters to get a fair compensation estimate.")


@st.cache_resource
def load_model():
    return joblib.load(model_path)


model = load_model()

with st.form("employee_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Employee Age", min_value=18, max_value=70, value=25)
        experience = st.number_input(
            "Years of Experience", min_value=0.0, max_value=50.0, value=2.0
        )
        education = st.selectbox(
            "Education Level", ["High School", "Bachelor", "Master", "PhD"]
        )
        job_role = st.selectbox(
            "Job Role",
            [
                "Software Engineer",
                "Data Analyst",
                "DevOps",
                "Product Manager",
                "ML Engineer",
                "QA Engineer",
            ],
        )

    with col2:
        perf_score = st.slider(
            "Performance Score (1.0 - 5.0)",
            min_value=1.0,
            max_value=5.0,
            value=3.0,
            step=0.1,
        )
        skills = st.number_input(
            "Number of Technical Skills", min_value=1, max_value=20, value=5
        )
        city_tier = st.selectbox("City Tier", [1, 2, 3])
        remote = st.radio("Remote Work?", ["No", "Yes"])
        remote_val = 1 if remote == "Yes" else 0

    submit_button = st.form_submit_button(label="Calculate Salary Estimate")

# Logic Execution
if submit_button:
    # Bungkus dalam format DataFrame yang dikenali oleh scikit-learn pipeline
    input_data = pd.DataFrame(
        [
            {
                "age": age,
                "years_experience": experience,
                "education_level": education,
                "job_role": job_role,
                "performance_score": perf_score,
                "num_skills": skills,
                "city_tier": city_tier,
                "remote_work": remote_val,
            }
        ]
    )

    prediction = model.predict(input_data)[0]

    st.success(f"### Estimated Annual Salary: **${prediction:,.2f} USD**")
    st.info(
        "This forecast was generated using the Ridge Regression Pipeline, with a historical R² accuracy of 98.5%."
    )
