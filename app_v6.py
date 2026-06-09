# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 22:41:27 2026

@author: firda
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import re

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Fault Intelligence Platform",
    page_icon="🚨",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

[data-testid="stMetricValue"] {
    font-size: 28px;
}

[data-testid="metric-container"] {
    background-color: #1B263B;
    border: 1px solid #2E4057;
    padding: 15px;
    border-radius: 12px;
}

h1,h2,h3 {
    color:white;
}

</style>
""", unsafe_allow_html=True)

st.title("🚨 Operational Fault Intelligence Platform")
st.caption("Fault Analytics • Risk Analysis • Downtime Intelligence")

# ==========================================
# DOWNTIME CONVERTER
# ==========================================

def convert_downtime_to_minutes(value):

    if pd.isna(value):
        return 0

    text = str(value).lower()

    total_minutes = 0

    # Days
    days = re.search(r'(\d+)\s*day', text)
    if days:
        total_minutes += int(days.group(1)) * 1440

    # Hours
    hours = re.search(r'(\d+)\s*(hour|hr)', text)
    if hours:
        total_minutes += int(hours.group(1)) * 60

    # Minutes
    minutes = re.search(r'(\d+)\s*(minute|min)', text)
    if minutes:
        total_minutes += int(minutes.group(1))

    # Seconds
    seconds = re.search(r'(\d+)\s*(second|sec)', text)
    if seconds:
        total_minutes += round(int(seconds.group(1)) / 60, 2)

    return total_minutes



# ==========================================
# FILE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload Fault Report",
    type=["xlsx", "xls"]
)

if uploaded_file is None:
    st.info("📁 Upload an Excel file to begin analysis.")
    st.stop()

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_excel(uploaded_file)

df["Open Time"] = pd.to_datetime(
    df["Open Time"],
    errors="coerce"
)

df["Downtime_Minutes"] = (
    df["Down Time"]
    .apply(convert_downtime_to_minutes)
)

def format_downtime(minutes):

    days = int(minutes // 1440)
    hours = int((minutes % 1440) // 60)
    mins = int(minutes % 60)

    if days > 0:
        return f"{days}d {hours}h"

    if hours > 0:
        return f"{hours}h {mins}m"

    return f"{mins}m"

df["Downtime_Display"] = (
    df["Downtime_Minutes"]
    .apply(format_downtime)
)

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Dashboard Filters")

location_filter = st.sidebar.multiselect(
    "Location",
    sorted(df["Location"].dropna().unique())
)

category_filter = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].dropna().unique())
)

severity_filter = st.sidebar.multiselect(
    "Severity",
    sorted(df["Severity"].dropna().unique())
)

type_filter = st.sidebar.multiselect(
    "Type",
    sorted(df["Type"].dropna().unique())
)

filtered_df = df.copy()

if location_filter:
    filtered_df = filtered_df[
        filtered_df["Location"].isin(location_filter)
    ]

if category_filter:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(category_filter)
    ]

if severity_filter:
    filtered_df = filtered_df[
        filtered_df["Severity"].isin(severity_filter)
    ]

if type_filter:
    filtered_df = filtered_df[
        filtered_df["Type"].isin(type_filter)
    ]

# ==========================================
# OPERATIONAL HEALTH SCORE
# ==========================================

total_faults = len(filtered_df)

avg_downtime_hours = (
    filtered_df["Downtime_Minutes"].mean() / 60
)

emergency_count = (
    filtered_df["Severity"]
    .astype(str)
    .str.contains("Emergency", case=False, na=False)
    .sum()
)

health_score = 100

health_score -= min(total_faults * 0.05, 25)
health_score -= min(emergency_count * 2, 25)
health_score -= min(avg_downtime_hours * 0.1, 25)

health_score = max(0, round(health_score))

if health_score >= 80:
    status = "🟢 Stable"
elif health_score >= 60:
    status = "🟡 Warning"
else:
    status = "🔴 Critical"

# ==========================================
# KPI DASHBOARD
# ==========================================

st.markdown("""
## 📊 Executive Operations Dashboard
Real-Time Fault Analytics & Downtime Intelligence
""")

st.metric(
    "🏥 Operational Health Score",
    f"{health_score}/100",
    status
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Faults",
    f"{len(filtered_df):,}"
)

c2.metric(
    "Locations",
    filtered_df["Location"].nunique()
)

c3.metric(
    "Categories",
    filtered_df["Category"].nunique()
)

c4.metric(
    "Fault Types",
    filtered_df["Type"].nunique()
)

c5.metric(
    "Avg Downtime (hrs)",
    round(
        filtered_df["Downtime_Minutes"].mean() / 60,
        1
    )
)

st.divider()

# ==========================================
# TREND INTELLIGENCE
# ==========================================

st.subheader("📈 Trend Intelligence")

trend_df = filtered_df.copy()

trend_df = trend_df.dropna(
    subset=["Open Time"]
)

trend_df["Date"] = (
    trend_df["Open Time"]
    .dt.date
)

daily_trend = (
    trend_df.groupby("Date")
    .size()
    .reset_index(name="Fault Count")
)

fig_trend = px.line(
    daily_trend,
    x="Date",
    y="Fault Count",
    markers=True,
    title="Fault Volume Over Time"
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

st.divider()

# ==========================================
# DOWNTIME INTELLIGENCE
# ==========================================

st.subheader("⏱️ Downtime Intelligence")

total_downtime_hours = round(
    filtered_df["Downtime_Minutes"].sum() / 60,
    1
)

location_downtime = (
    filtered_df.groupby("Location")["Downtime_Minutes"]
    .sum()
    .sort_values(ascending=False)
)

category_downtime = (
    filtered_df.groupby("Category")["Downtime_Minutes"]
    .sum()
    .sort_values(ascending=False)
)

fault_downtime = (
    filtered_df.groupby("Type")["Downtime_Minutes"]
    .sum()
    .sort_values(ascending=False)
)

top_location = location_downtime.index[0]
top_location_hours = round(
    location_downtime.iloc[0] / 60,
    1
)

top_category = category_downtime.index[0]
top_category_hours = round(
    category_downtime.iloc[0] / 60,
    1
)

top_fault = fault_downtime.index[0]
top_fault_hours = round(
    fault_downtime.iloc[0] / 60,
    1
)

d1, d2, d3, d4 = st.columns(4)

d1.metric(
    "Total Downtime (hrs)",
    f"{total_downtime_hours:,.0f}"
)

d2.metric(
    "Worst Location",
    top_location
)

d3.metric(
    "Worst Category",
    top_category
)

d4.metric(
    "Worst Fault Type",
    top_fault
)

st.caption(
    f"""
Highest downtime location:
{top_location} ({top_location_hours:,.1f} hrs)

Highest downtime category:
{top_category} ({top_category_hours:,.1f} hrs)

Highest downtime fault:
{top_fault} ({top_fault_hours:,.1f} hrs)
"""
)

col_dt1, col_dt2 = st.columns(2)

with col_dt1:

    st.subheader("📍 Top Locations by Downtime")

    fig_dt1 = px.bar(
        location_downtime.head(10).reset_index(),
        x="Location",
        y="Downtime_Minutes"
    )

    st.plotly_chart(
        fig_dt1,
        use_container_width=True
    )

with col_dt2:

    st.subheader("🚨 Top Fault Types by Downtime")

    fig_dt2 = px.bar(
        fault_downtime.head(10).reset_index(),
        x="Type",
        y="Downtime_Minutes"
    )

    st.plotly_chart(
        fig_dt2,
        use_container_width=True
    )

st.divider()

# ==========================================
# RISK INTELLIGENCE
# ==========================================

st.subheader("🚨 Critical Risk Ranking")

risk_df = (
    filtered_df.groupby("Category")
    .agg(
        Fault_Count=("Category", "count"),
        Avg_Downtime=("Downtime_Minutes", "mean")
    )
    .reset_index()
)

risk_df["Risk Score"] = (
    risk_df["Fault_Count"] *
    risk_df["Avg_Downtime"]
)

risk_df["Avg_Downtime_Hours"] = (
    risk_df["Avg_Downtime"] / 60
).astype(int)

risk_df["Risk Score"] = (
    risk_df["Risk Score"]
    .round(0)
    .astype(int)
)

risk_df = risk_df.sort_values(
    "Risk Score",
    ascending=False
)

risk_df = risk_df.reset_index(drop=True)

risk_df.insert(
    0,
    "Rank",
    range(1, len(risk_df) + 1)
)

risk_df = risk_df.reset_index(drop=True)



risk_df = risk_df[
    [
        "Category",
        "Fault_Count",
        "Avg_Downtime_Hours",
        "Risk Score"
    ]
]

risk_df = risk_df.rename(
    columns={
        "Fault_Count": "Fault Count",
        "Avg_Downtime_Hours": "Avg Downtime (hrs)"
    }
)

st.dataframe(
    risk_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# CRITICAL FAULT RADAR
# ==========================================

st.divider()

st.subheader("🚨 Critical Fault Radar")

severity_weights = {
    "Emergency": 5,
    "Urgent": 3,
    "Normal": 1
}

radar_df = filtered_df.copy()

radar_df["Weight"] = (
    radar_df["Severity"]
    .map(severity_weights)
    .fillna(1)
)

radar_df["Impact Score"] = (
    radar_df["Downtime_Minutes"]
    * radar_df["Weight"]
)

impact_summary = (
    radar_df.groupby("Type")["Impact Score"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_radar = px.bar(
    impact_summary,
    x="Type",
    y="Impact Score",
    title="Highest Operational Impact Faults"
)

st.plotly_chart(
    fig_radar,
    use_container_width=True
)

# ==========================================
# CHART ROW 1
# ==========================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🚨 Severity Distribution")

    severity_counts = (
        filtered_df["Severity"]
        .value_counts()
        .reset_index()
    )

    severity_counts.columns = [
        "Severity",
        "Count"
    ]

    fig = px.bar(
        severity_counts,
        x="Severity",
        y="Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("📂 Category Distribution")

    category_counts = (
        filtered_df["Category"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    category_counts.columns = [
        "Category",
        "Count"
    ]

    fig2 = px.pie(
        category_counts,
        names="Category",
        values="Count"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================================
# CHART ROW 2
# ==========================================

col3, col4 = st.columns(2)

with col3:

    st.subheader("🔧 Top Fault Types")

    type_counts = (
        filtered_df["Type"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    type_counts.columns = [
        "Type",
        "Count"
    ]

    fig3 = px.bar(
        type_counts,
        x="Type",
        y="Count"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col4:

    st.subheader("📍 Top Fault Locations")

    location_counts = (
        filtered_df["Location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    location_counts.columns = [
        "Location",
        "Count"
    ]

    fig4 = px.bar(
        location_counts,
        x="Location",
        y="Count"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ==========================================
# AI INSIGHTS
# ==========================================

st.divider()

st.subheader("🤖 AI Executive Insights")

top_location = filtered_df["Location"].value_counts().idxmax()
top_type = filtered_df["Type"].value_counts().idxmax()

emergency_count = (
    filtered_df["Severity"]
    .astype(str)
    .str.contains(
        "Emergency",
        case=False,
        na=False
    )
    .sum()
)

emergency_pct = round(
    emergency_count /
    len(filtered_df) * 100,
    2
)

st.info(f"""
EXECUTIVE SUMMARY

Analysis of {len(filtered_df):,} operational faults identified
'{top_type}' as the most frequently occurring fault type.

The highest concentration of incidents occurred at
'{top_location}'.

The fault type generating the greatest operational impact was
'{top_fault}', contributing approximately
{top_fault_hours:,.1f} downtime hours.

Emergency incidents accounted for
{emergency_pct}% of all recorded faults.

RECOMMENDATIONS

• Prioritise preventive maintenance at high-frequency locations.

• Investigate recurring causes of '{top_fault}'.

• Focus resources on critical categories identified in the Risk Matrix.

• Continue monitoring fault trends to minimise operational disruption.
""")

# ==========================================
# EXECUTIVE REPORT GENERATOR
# ==========================================

st.divider()

st.subheader("📄 Executive Report Generator")

if st.button("Generate Executive Report"):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    report = []

    report.append(
        Paragraph(
            "Operational Fault Intelligence Platform",
            styles["Title"]
        )
    )

    report.append(
        Paragraph(
            "Executive Fault Analysis Report",
            styles["Heading2"]
        )
    )

    report.append(Spacer(1,12))

    report.append(
        Paragraph(
            f"Total Faults: {len(filtered_df):,}",
            styles["BodyText"]
        )
    )

    report.append(
        Paragraph(
            f"Most Common Fault Type: {top_type}",
            styles["BodyText"]
        )
    )

    report.append(
        Paragraph(
            f"Most Problematic Location: {top_location}",
            styles["BodyText"]
        )
    )

    report.append(
        Paragraph(
            f"Highest Downtime Fault: {top_fault}",
            styles["BodyText"]
        )
    )

    report.append(
        Paragraph(
            f"Highest Downtime Fault Hours: {top_fault_hours:,.1f}",
            styles["BodyText"]
        )
    )

    report.append(
        Paragraph(
            f"Emergency Fault Percentage: {emergency_pct}%",
            styles["BodyText"]
        )
    )

    report.append(Spacer(1,20))

    report.append(
        Paragraph(
            "Executive Recommendations",
            styles["Heading2"]
        )
    )

    report.append(
        Paragraph(
            """
            Prioritise preventive maintenance at
            high-frequency locations.

            Investigate recurring causes of
            high-downtime fault categories.

            Focus operational resources on
            critical fault trends and downtime
            reduction initiatives.
            """,
            styles["BodyText"]
        )
    )

    doc.build(report)

    pdf = buffer.getvalue()

    st.download_button(
        label="📥 Download Executive Report",
        data=pdf,
        file_name="Executive_Fault_Report.pdf",
        mime="application/pdf"
    )

# ==========================================
# FAULT EXPLORER
# ==========================================

st.divider()

st.subheader("🔎 Fault Explorer")

search_term = st.text_input(
    "Search Details"
)

if search_term:

    display_df = filtered_df[
        filtered_df["Details"]
        .astype(str)
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    ]

else:

    display_df = filtered_df

display_df = display_df.drop(
    columns=["Down Time"],
    errors="ignore"
)

display_df = display_df.drop(
    columns=["Downtime_Minutes"],
    errors="ignore"
)

display_df = display_df.rename(
    columns={
        "Downtime_Display": "Downtime"
    }
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.caption(
    "Operational Fault Intelligence Platform (OFIP) v2.0 | Built with Python, Streamlit & AI Analytics - by Firdaus"
)
