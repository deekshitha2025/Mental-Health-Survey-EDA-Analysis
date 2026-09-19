# ============================================================
# MENTAL HEALTH IN TECH SURVEY - STREAMLIT APP
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="Mental Health in Tech",
    page_icon="🧠",
    layout="wide"
)

# ------------------------------------------------------------
# Title
# ------------------------------------------------------------

st.title("🧠 Mental Health in Tech Survey")

st.markdown(
    """
    ### 📊 Interactive Mental Health Analytics Dashboard

    Explore mental health attitudes, treatment, workplace
    support, remote work and employee experiences.
    """
)

# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------

@st.cache_data
def load_data():

    data = pd.read_csv("survey.csv")

    # Remove duplicates
    data = data.drop_duplicates()

    # Clean Age
    data = data[
        (data["Age"] >= 18) &
        (data["Age"] <= 70)
    ]

    return data


df = load_data()

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

st.sidebar.header("🔎 Filters")

# Country filter
countries = sorted(
    df["Country"].dropna().unique().tolist()
)

selected_country = st.sidebar.multiselect(
    "Select Country",
    countries
)

# Gender filter
genders = sorted(
    df["Gender"].dropna().unique().tolist()
)

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    genders
)

# Treatment filter
treatments = sorted(
    df["treatment"].dropna().unique().tolist()
)

selected_treatment = st.sidebar.multiselect(
    "Treatment",
    treatments
)

# Remote work filter
remote_options = sorted(
    df["remote_work"].dropna().unique().tolist()
)

selected_remote = st.sidebar.multiselect(
    "Remote Work",
    remote_options
)

# ------------------------------------------------------------
# Apply Filters
# ------------------------------------------------------------

filtered_df = df.copy()

if selected_country:
    filtered_df = filtered_df[
        filtered_df["Country"].isin(selected_country)
    ]

if selected_gender:
    filtered_df = filtered_df[
        filtered_df["Gender"].isin(selected_gender)
    ]

if selected_treatment:
    filtered_df = filtered_df[
        filtered_df["treatment"].isin(selected_treatment)
    ]

if selected_remote:
    filtered_df = filtered_df[
        filtered_df["remote_work"].isin(selected_remote)
    ]

# ------------------------------------------------------------
# KPI Calculations
# ------------------------------------------------------------

total_respondents = len(filtered_df)

treatment_percentage = (
    (filtered_df["treatment"] == "Yes").mean() * 100
    if len(filtered_df) > 0
    else 0
)

family_history_percentage = (
    (filtered_df["family_history"] == "Yes").mean() * 100
    if len(filtered_df) > 0
    else 0
)

remote_percentage = (
    (filtered_df["remote_work"] == "Yes").mean() * 100
    if len(filtered_df) > 0
    else 0
)

# ------------------------------------------------------------
# KPI Cards
# ------------------------------------------------------------

st.subheader("📌 Key Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Respondents",
    total_respondents
)

col2.metric(
    "🧠 Treatment %",
    f"{treatment_percentage:.1f}%"
)

col3.metric(
    "❤️ Family History %",
    f"{family_history_percentage:.1f}%"
)

col4.metric(
    "🏠 Remote Work %",
    f"{remote_percentage:.1f}%"
)

st.divider()

# ============================================================
# ROW 1
# ============================================================

col1, col2 = st.columns(2)

# ------------------------------------------------------------
# Treatment Chart
# ------------------------------------------------------------

with col1:

    st.subheader("🧠 Mental Health Treatment")

    treatment_data = (
        filtered_df["treatment"]
        .value_counts()
        .reset_index()
    )

    treatment_data.columns = [
        "Treatment",
        "Count"
    ]

    fig = px.pie(
        treatment_data,
        names="Treatment",
        values="Count",
        title="Treatment Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------------------------------------------
# Age Distribution
# ------------------------------------------------------------

with col2:

    st.subheader("👤 Age Distribution")

    fig = px.histogram(
        filtered_df,
        x="Age",
        nbins=20,
        title="Age Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# ROW 2
# ============================================================

col1, col2 = st.columns(2)

# ------------------------------------------------------------
# Family History vs Treatment
# ------------------------------------------------------------

with col1:

    st.subheader("❤️ Family History vs Treatment")

    family_data = (
        filtered_df
        .groupby(
            ["family_history", "treatment"]
        )
        .size()
        .reset_index(
            name="Count"
        )
    )

    fig = px.bar(
        family_data,
        x="family_history",
        y="Count",
        color="treatment",
        barmode="group",
        title="Family History and Treatment"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------------------------------------------
# Gender Distribution
# ------------------------------------------------------------

with col2:

    st.subheader("👥 Gender Distribution")

    gender_data = (
        filtered_df["Gender"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    gender_data.columns = [
        "Gender",
        "Count"
    ]

    fig = px.bar(
        gender_data,
        x="Gender",
        y="Count",
        title="Gender Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# ROW 3
# ============================================================

col1, col2 = st.columns(2)

# ------------------------------------------------------------
# Benefits vs Treatment
# ------------------------------------------------------------

with col1:

    st.subheader("🏢 Benefits vs Treatment")

    benefits_data = (
        filtered_df
        .groupby(
            ["benefits", "treatment"]
        )
        .size()
        .reset_index(
            name="Count"
        )
    )

    fig = px.bar(
        benefits_data,
        x="benefits",
        y="Count",
        color="treatment",
        barmode="group",
        title="Employer Benefits vs Treatment"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------------------------------------------
# Remote Work vs Treatment
# ------------------------------------------------------------

with col2:

    st.subheader("🏠 Remote Work vs Treatment")

    remote_data = (
        filtered_df
        .groupby(
            ["remote_work", "treatment"]
        )
        .size()
        .reset_index(
            name="Count"
        )
    )

    fig = px.bar(
        remote_data,
        x="remote_work",
        y="Count",
        color="treatment",
        barmode="group",
        title="Remote Work vs Treatment"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# COUNTRY ANALYSIS
# ============================================================

st.divider()

st.subheader("🌍 Geographic Analysis")

country_data = (
    filtered_df["Country"]
    .value_counts()
    .head(15)
    .reset_index()
)

country_data.columns = [
    "Country",
    "Respondents"
]

fig = px.bar(
    country_data,
    x="Country",
    y="Respondents",
    title="Top 15 Countries by Respondents"
)

fig.update_xaxes(
    tickangle=45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# WORK INTERFERENCE
# ============================================================

st.subheader("💼 Mental Health and Work Interference")

work_data = (
    filtered_df["work_interfere"]
    .value_counts()
    .reset_index()
)

work_data.columns = [
    "Work Interference",
    "Count"
]

fig = px.bar(
    work_data,
    x="Work Interference",
    y="Count",
    title="Mental Health Work Interference"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# MENTAL VS PHYSICAL HEALTH
# ============================================================

st.subheader("⚖️ Mental Health vs Physical Health")

mental_physical = (
    filtered_df["mental_vs_physical"]
    .value_counts()
    .reset_index()
)

mental_physical.columns = [
    "Response",
    "Count"
]

fig = px.pie(
    mental_physical,
    names="Response",
    values="Count",
    title="Does Employer Take Mental Health as Seriously?"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# SUPERVISOR
# ============================================================

st.subheader("👨‍💼 Discussing Mental Health with Supervisor")

supervisor_data = (
    filtered_df["supervisor"]
    .value_counts()
    .reset_index()
)

supervisor_data.columns = [
    "Response",
    "Count"
]

fig = px.bar(
    supervisor_data,
    x="Response",
    y="Count",
    title="Willingness to Discuss Mental Health with Supervisor"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# DATA TABLE
# ============================================================

st.divider()

st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    ### 📌 Project Summary

    This dashboard analyzes mental health attitudes and
    experiences in the technology workplace.

    **Tools Used:** Python, Pandas, NumPy, Plotly and Streamlit
    """
)