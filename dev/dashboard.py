import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Interactive Dashboard")


@st.cache_data
def load_data():
    df = pd.read_csv("employee_salary_regression.csv")
    return df


df = load_data()

filter1, filter2, filter3 = st.columns(3)

with filter1:
    edu = st.multiselect(
        "Select a Level of Education",
        options=["High School", "Bachelor", "Master", "PhD"],
        default=df["education_level"].unique(),
    )
with filter2:
    role = st.selectbox(
        "Select a Job Role",
        options=["Semua"] + list(df["job_role"].unique()),
    )
with filter3:
    tier_list = sorted(df["city_tier"].unique())
    city = st.multiselect(
        "Select City Tier",
        options=tier_list,
        default=tier_list,
    )

st.divider()

filter4, filter5 = st.columns(2)

with filter4:
    exp = st.slider(
        "Work Experience",
        min_value=df["years_experience"].min(),
        max_value=df["years_experience"].max(),
        value=(df["years_experience"].min(), df["years_experience"].max()),
        step=1,
    )
with filter5:
    perf = st.slider(
        "Performance Score",
        min_value=df["performance_score"].min(),
        max_value=df["performance_score"].max(),
        value=(df["performance_score"].min(), df["performance_score"].max()),
    )


data = df.copy()

data = data[data["education_level"].isin(edu)]
data = data[data["city_tier"].isin(city)]
if role != "Semua":
    data = data[data["job_role"] == role]

data = data[data["years_experience"].between(exp[0], exp[1])]
data = data[data["performance_score"].between(perf[0], perf[1])]

# if edu is not None:
#     data = data[data["education_level"].isin(edu)]

# if exp is not None:
#     data = data[
#         (data["years_experience"] >= exp[0]) & (data["years_experience"] <= exp[1])
#     ]

met1, met2, met3 = st.columns(3)
with met1:
    value1 = data["employee_id"].count()
    perc = round(data["employee_id"].count() / df["employee_id"].count() * 100)
    cd1 = data.groupby("job_role").size()
    if "prev_value" not in st.session_state:
        st.session_state.prev_value = 0
    new_value = data["employee_id"].count()
    delta = new_value - st.session_state.prev_value
    st.session_state.prev_value = new_value

    st.metric(
        "Number of Employees",
        f"{value1} Employees",
        delta=delta,
        border=True,
        chart_data=cd1,
        chart_type="bar",
        delta_description=f"{perc}% of total employees",
    )

with met2:
    value2 = data["annual_salary_usd"].mean()
    perc = round(
        data["annual_salary_usd"].mean() / df["annual_salary_usd"].mean() * 100
    )
    cd2 = round(data.groupby("job_role")["annual_salary_usd"].mean())
    if "prev_value2" not in st.session_state:
        st.session_state.prev_value2 = 0
    new_value2 = round(data["annual_salary_usd"].mean())
    delta2 = new_value2 - st.session_state.prev_value2
    st.session_state.prev_value2 = new_value2
    st.metric(
        "Average Salary",
        f"${value2:,.2f}",
        chart_data=cd2,
        chart_type="line",
        delta=delta2,
        delta_description=f"{perc}% of average salary",
        border=True,
    )

with met3:
    value3 = data["years_experience"].mean()
    perc = round(data["years_experience"].mean() / df["years_experience"].mean() * 100)
    cd3 = round(data.groupby("job_role")["years_experience"].mean())
    if "prev_value3" not in st.session_state:
        st.session_state.prev_value3 = 0
    new_value3 = round(data["years_experience"].mean())
    delta3 = new_value3 - st.session_state.prev_value3
    st.session_state.prev_value3 = new_value3
    st.metric(
        "Average Experience",
        f"{value3:.1f} Years",
        delta=delta3,
        delta_description=f"{perc}% of average experience",
        chart_data=cd3,
        chart_type="area",
        border=True,
    )

st.divider()

st.dataframe(data)

st.subheader("Charts")

chart1, chart2 = st.columns(2)

with chart1:
    st.write("Salary by Job Role")
    st.markdown("> Colors: Education Level")
    salary_job = df.pivot_table(
        index="job_role",
        columns="education_level",
        values="annual_salary_usd",
        aggfunc="mean",
    )

    st.bar_chart(salary_job)
with chart2:
    st.write("Education Level Distribution")
    st.markdown("> Colors: Job Role")
    edu_dist = df.pivot_table(
        index="education_level",
        columns="job_role",
        aggfunc="size",
    )
    st.bar_chart(edu_dist)

st.divider()

chart3, chart4 = st.columns(2)
with chart3:
    st.write("Exp and Age Correlation")
    st.markdown("> Colors: Education Level")
    st.scatter_chart(data, x="years_experience", y="age", color="education_level")
with chart4:
    st.write("Exp and Performance Correlation")
    st.markdown("> Colors: Education Level")
    st.scatter_chart(
        data, x="years_experience", y="performance_score", color="education_level"
    )

st.divider()

sal_exp = data.pivot_table(
    index="years_experience",
    columns="education_level",
    values="annual_salary_usd",
    aggfunc="mean",
)
st.write("Salary By Experience")
st.markdown("> Colors: Education Level")
st.line_chart(sal_exp, x_label="Experience", y_label="Avg Salary")
