import streamlit as st
import pandas as pd
import joblib

with st.expander("Tentang App & Ringkasan Insight Dataset"):
    st.markdown("""
    ### Informasi Umum Dataset
    Aplikasi ini dibangun menggunakan dataset *employee_salary_regression.csv*. 
    Model dilatih menggunakan metode **Ridge Regression Pipeline** dengan tingkat akurasi **$R^2$ mencapai 98.51%**. Artinya, 
    hampir seluruh variasi gaji di dalam perusahaan ini ditentukan oleh faktor-faktor terukur di bawah ini.

    ### Ringkasan Insight Utama (Data-Driven)
    Berdasarkan analisis regresi statistik mendalam, berikut adalah aturan rahasia di balik struktur penggajian:

    1. **Pengalaman Kerja adalah Driver Utama (Kontribusi ~84%)**
       Setiap tambahan **1 tahun pengalaman** secara konsisten menaikkan gaji sebesar **+$2.842 USD/tahun** (jika faktor lain sama).
    
    2. **Kinerja Dibayar Mahal**
       Peningkatan **1 poin pada Skor Performa** (misal dari 3.0 ke 4.0) memberikan lompatan gaji instan sebesar **+$6.219 USD/tahun**.
    
    3. **Penalti Geografis yang Masif**
       Lokasi kantor sangat memengaruhi kompensasi. Karyawan yang ditempatkan di kota **Tier 2 atau Tier 3** menerima potongan standar masing-masing sebesar **-$8.098 USD** per tingkat tier dibandingkan Tier 1.
    
    4. **Premi Kerja Remote**
       Karyawan dengan status *Remote Work* mendapatkan insentif tambahan sebesar **+$2.805 USD/tahun** dibandingkan pekerja *on-site*.
    
    5. **Nilai Finansial Sebuah Skill**
       Setiap penambahan **1 keahlian teknis (skill)** baru berkontribusi menaikkan gaji tahunan sebesar **+$1.211 USD**.

    ### Mitos yang Terbantahkan oleh Data
    * **Usia (Age):** Secara statistik tidak signifikan ($P\text{-value} = 0.643$). Usia biologis atau senioritas umur tidak memengaruhi besaran gaji jika jumlah pengalaman kerjanya sama.
    * **Jabatan (Job Role):** Perbedaan posisi (misal *ML Engineer* vs *Software Engineer*) tidak memberikan dampak independen terhadap gaji ($P\text{-value} = 0.775$) setelah faktor pengalaman dan jumlah skill dikontrol.
    """)

    st.image(
        "actual_vs_predicted.png",
        caption="Grafik Evaluasi Model: Aktual vs Prediksi Gaji",
    )
    st.image(
        "correlation_features.png",
        caption="Grafik Heatmap Korelasi antar Fitur",
    )
    st.subheader("Laporan Regresi Statistik Statsmodels")
    df_tabel = pd.read_csv("tabel_statistik_gaji.csv")
    st.dataframe(df_tabel, use_container_width=True)

    st.write("Pelajari lebih lanjut")

    col1, col2 = st.columns(2)

    with col1:
        # Tombol untuk GitHub
        st.link_button(
            "View Source Code on GitHub",
            "https://github.com/username/repo",
            use_container_width=True,
        )

    with col2:
        # Tombol untuk Kaggle
        st.link_button(
            "Download Data on Kaggle",
            "https://www.kaggle.com/datasets/alitaqishah/employee-compensation-and-salary-prediction-dataset",
            use_container_width=True,
        )

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
