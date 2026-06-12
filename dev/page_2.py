import streamlit as st
import pandas as pd

st.title("Dataset dan Insight")
with st.expander("Tentang dataset"):
    st.markdown(
        """
    ### Informasi Umum Dataset
    Aplikasi ini dibangun menggunakan dataset *employee_salary_regression.csv*. 
    Model dilatih menggunakan metode **Ridge Regression Pipeline** dengan tingkat akurasi **$R^2$ mencapai 98.51%**. Artinya, 
    hampir seluruh variasi gaji di dalam perusahaan ini ditentukan oleh faktor-faktor terukur di bawah ini."""
    )

with st.expander(" Ringkasan Insight Dataset"):
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
