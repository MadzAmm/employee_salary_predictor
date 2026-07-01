import streamlit as st
import pandas as pd
import os

current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, "actual_vs_predicted.png")
image_path2 = os.path.join(current_dir, "correlation_features.png")
csv_path = os.path.join(current_dir, "tabel_statistik_gaji.csv")

st.set_page_config(page_title="About Datasets and Insights", layout="centered")
st.title("Dataset and Insights")
with st.expander("About the dataset"):
    st.markdown(
        """
    ### Informasi Umum Dataset
    Aplikasi ini dibangun menggunakan dataset *employee_salary_regression.csv*. 
    Model dilatih menggunakan metode **Ridge Regression Pipeline** dengan tingkat akurasi **$R^2$ mencapai 98.51%**. Artinya, 
    hampir seluruh variasi gaji di dalam perusahaan ini ditentukan oleh faktor-faktor terukur di bawah ini."""
    )

with st.expander(" Dataset Insights Summary"):
    st.markdown("""
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
        image_path,
        caption="Grafik Evaluasi Model: Aktual vs Prediksi Gaji",
    )
    st.image(
        image_path2,
        caption="Grafik Heatmap Korelasi antar Fitur",
    )
    st.subheader("Statsmodels Statistical Regression Report")
    df_tabel = pd.read_csv(csv_path)
    st.dataframe(df_tabel, use_container_width=True)

st.write("Learn more")

col1, col2 = st.columns(2)

with col1:
    # Tombol untuk GitHub
    st.link_button(
        "View Source Code on GitHub",
        "https://github.com/MadzAmm/employee_salary_predictor",
        use_container_width=True,
    )

with col2:
    # Tombol untuk Kaggle
    st.link_button(
        "Download Data on Kaggle",
        "https://www.kaggle.com/datasets/alitaqishah/employee-compensation-and-salary-prediction-dataset",
        use_container_width=True,
    )
