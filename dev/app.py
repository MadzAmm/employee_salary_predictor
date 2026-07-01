import streamlit as st
import pandas as pd
import joblib

main_page = st.Page("main_page.py", title="Employee Salary Forecast")
about_page = st.Page("about.py", title="About Datasets and Insights")
dashboard_page = st.Page("dashboard.py", title="Dashboard")

# Set up navigation
pg = st.navigation([main_page, about_page, dashboard_page])

# Run the selected page
pg.run()
