import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Estimasi Gaji Karyawan", layout="centered")
st.title("Sistem Prediksi Gaji Karyawan")
st.write("Masukkan parameter karyawan untuk mendapatkan estimasi kompensasi yang adil.")


@st.cache_resource
def load_model():
    return joblib.load("lr_salary_model.pkl")


model = load_model()

with st.form("employee_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Umur Karyawan", min_value=18, max_value=70, value=25)
        experience = st.number_input(
            "Pengalaman Kerja (Tahun)", min_value=0.0, max_value=50.0, value=2.0
        )
        education = st.selectbox(
            "Tingkat Pendidikan", ["High School", "Bachelor", "Master", "PhD"]
        )
        job_role = st.selectbox(
            "Role Pekerjaan",
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
            "Skor Performa (1.0 - 5.0)",
            min_value=1.0,
            max_value=5.0,
            value=3.0,
            step=0.1,
        )
        skills = st.number_input(
            "Jumlah Keahlian Teknis", min_value=1, max_value=20, value=5
        )
        city_tier = st.selectbox("Tingkat Kota (Tier)", [1, 2, 3])
        remote = st.radio("Sistem Kerja Remote?", ["Tidak", "Ya"])
        remote_val = 1 if remote == "Ya" else 0

    submit_button = st.form_submit_button(label="Hitung Estimasi Gaji")

# Logic Eksekusi
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

    st.success(f"### Estimasi Gaji Tahunan: **${prediction:,.2f} USD**")
    st.info(
        "Prediksi ini diproses menggunakan Ridge Regression Pipeline dengan akurasi historis R² 98.5%."
    )
