import streamlit as st

main_page = st.Page("main_page.py", title="Prediksi Gaji Karyawan")
page_2 = st.Page("page_2.py", title="Tentang Dataset dan Insight")
# Set up navigation
pg = st.navigation([main_page, page_2])

# Run the selected page
pg.run()
