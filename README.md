# Sistem Prediksi Gaji Karyawan

## Overview

Aplikasi _machine learning_ berstandar produksi yang dirancang untuk mengestimasi dan menganalisis kompensasi karyawan. Dibangun menggunakan Streamlit dan Scikit-Learn, aplikasi ini memproses metrik demografi, metrik performa, dan peran kerja untuk menghasilkan estimasi gaji yang presisi dan didukung oleh pemodelan statistik yang kuat. Sistem ini secara khusus dirancang untuk memberikan wawasan sumber daya manusia yang berbasis data melalui antarmuka web yang intuitif dan interaktif.

## Key Features

- **Advanced Predictive Modeling**: Memanfaatkan algoritma Regresi Linear dengan Regularisasi L2 (Ridge) untuk memastikan peramalan tingkat kompensasi dengan akurasi tinggi.
- **Automated Data Pipeline**: Mengimplementasikan prapemrosesan data secara terpusat menggunakan `ColumnTransformer` dari Scikit-Learn untuk standardisasi skala, _ordinal encoding_, dan _one-hot encoding_, yang secara ketat mencegah kebocoran data (_data leakage_).
- **Statistical Interpretability**: Mengintegrasikan metodologi _Ordinary Least Squares_ (OLS) untuk menyediakan analisis dampak finansial secara transparan pada setiap fitur dan ekstraksi koefisien absolut.
- **Interactive Dashboard**: Antarmuka pengguna yang bersih dan responsif yang dibangun dengan Streamlit, memungkinkan penyesuaian parameter secara _real-time_ dan evaluasi performa model secara visual.

## Technology Stack

- **Core Runtime**: Python 3.x
- **Machine Learning**: Scikit-Learn, Statsmodels
- **Data Engineering**: Pandas, NumPy
- **Frontend / Deployment**: Streamlit
- **Visualization**: Matplotlib, Seaborn
