import streamlit as st
import pandas as pd
import joblib

main_page = st.Page("main_page.py", title="Prediksi Gaji Karyawan")
about_page = st.Page("about.py", title="Tentang Dataset dan Insight")
# Set up navigation
pg = st.navigation([main_page, about_page])

# Run the selected page
pg.run()
