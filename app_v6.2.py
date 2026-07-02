# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 10:56:24 2026

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
    page_title="Fault Analysis System",
    page_icon="🚨",
    layout="wide"
)

st.markdown("""
<style>

/* ================================
BACKGROUND
================================ */

.stApp{

background:
radial-gradient(circle at top left,
rgba(68,199,255,.18),
transparent 35%),

radial-gradient(circle at top right,
rgba(168,85,247,.18),
transparent 35%),

radial-gradient(circle at bottom,
rgba(255,90,205,.10),
transparent 45%),

linear-gradient(
135deg,
#050816,
#081326,
#0b1022);

color:white;

}

.main .block-container{
    padding-top:2rem;
    padding-left:2rem;
    padding-right:2rem;
    max-width:1600px;
}

/* =================================
SIDEBAR
================================= */

[data-testid="stSidebar"]{

    background:linear-gradient(180deg,#0b1020,#111827);

    border-right:1px solid rgba(120,120,255,.25);

    box-shadow:
    0 0 30px rgba(110,70,255,.15);

}

[data-testid="stSidebar"] *{

    color:white;

}

/* =================================
HEADINGS
================================= */

h1{

    font-size:52px;

    font-weight:800;

    background:linear-gradient(
    90deg,
    #42a5ff,
    #7d7cff,
    #f472ff);

    -webkit-background-clip:text;

    -webkit-text-fill-color:transparent;

}

h2{

    color:white;

}

h3{

    color:#E5E7EB;

}

p,label{

    color:#B8C0D4;

}

/* =================================
UPLOAD BOX
================================= */

[data-testid="stFileUploader"]{

    border-radius:22px;

    border:1px solid rgba(80,120,255,.35);

    background:rgba(20,24,40,.55);

    backdrop-filter:blur(15px);

    padding:20px;

    box-shadow:
    0 0 40px rgba(77,125,255,.08);

}

/* =================================
METRIC CARDS
================================= */

[data-testid="stMetric"]{

    background:rgba(15,18,35,.65);

    border-radius:20px;

    border:1px solid rgba(90,120,255,.35);

    padding:22px;

    backdrop-filter:blur(12px);

    transition:.35s;

}

[data-testid="stMetric"]:hover{

    transform:translateY(-6px);

    box-shadow:

    0 0 15px #3B82F6,

    0 0 30px rgba(147,51,234,.35);

}

[data-testid="stMetricValue"]{

    color:white;

    font-size:38px;

    font-weight:800;

}

[data-testid="stMetricLabel"]{

    color:#94A3B8;

}

/* =================================
BUTTONS
================================= */

.stButton>button{

    background:linear-gradient(
    90deg,
    #3B82F6,
    #7C3AED);

    color:white;

    border:none;

    border-radius:14px;

    font-weight:700;

    padding:.6rem 1.2rem;

    transition:.3s;

}

.stButton>button:hover{

    transform:scale(1.05);

    box-shadow:

    0 0 20px #3B82F6,

    0 0 30px #7C3AED;

}

/* =================================
TABLE
================================= */

[data-testid="stDataFrame"]{

    background:#111827;

    border-radius:18px;

    border:1px solid rgba(255,255,255,.08);

}

/* =================================
EXPANDER
================================= */

div[data-testid="stExpander"]{

    background:#101826;

    border-radius:18px;

    border:1px solid rgba(255,255,255,.08);

}

/* =================================
PLOTLY
================================= */

.js-plotly-plot{

    border-radius:20px;

    background:rgba(20,24,40,.55);

}

/* =================================
SCROLLBAR
================================= */

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-thumb{

    background:#5B5EFF;

    border-radius:20px;

}
/* ===========================================
GRADIENT TEXT
=========================================== */

.gradient-title{

font-size:58px;
font-weight:900;

background:linear-gradient(
90deg,
#4FC3F7,
#7C4DFF,
#FF5ACD);

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;

text-shadow:
0 0 18px rgba(79,195,247,.35);

margin-bottom:6px;

}

.gradient-heading{

font-size:40px;
font-weight:800;

background:linear-gradient(
90deg,
#44C7FF,
#A855F7);

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;

}

.subtitle{

color:#A5B4FC;

font-size:18px;

margin-top:6px;

}

.section-note{

color:#8FA8D8;

font-size:15px;

}
/* ===========================================
KPI CARDS
=========================================== */

.kpi-card{

background:rgba(15,18,35,.78);

border:1px solid rgba(90,120,255,.25);

border-left:5px solid var(--accent);

border-radius:18px;

padding:18px;

height:145px;

transition:.3s;

box-shadow:

0 8px 40px rgba(0,0,0,.35),

0 0 25px rgba(68,199,255,.08),

0 0 40px rgba(168,85,247,.08);

}

.kpi-card:hover{

transform:translateY(-4px);

box-shadow:0 0 18px rgba(80,120,255,.25);

}

.kpi-title{

font-size:15px;

color:#9CA3AF;

font-weight:600;

margin-bottom:12px;

}

.kpi-value{

font-size:36px;

font-weight:800;

color:white;

}

.kpi-sub{

font-size:13px;

color:#7C8CA8;

margin-top:10px;

}

.cyber-divider{

height:2px;

margin:35px 0;

background:linear-gradient(
90deg,
transparent,
#44C7FF,
#8B5CF6,
#FF5ACD,
transparent);

box-shadow:
0 0 8px rgba(68,199,255,.35),
0 0 18px rgba(168,85,247,.25);

border-radius:999px;

}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='
font-size:64px;
font-weight:900;
margin-bottom:10px;
line-height:1.1;
background:linear-gradient(90deg,#39B8FF,#7C5CFF,#C471ED,#FF5ACD);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
text-shadow:0 0 25px rgba(100,150,255,.35);
'>

🚨 Operational Fault Dashboard

</h1>

<p style='
font-size:20px;
color:#A7B6D7;
margin-top:-8px;
margin-bottom:35px;
'>

Real-time fault analytics, downtime intelligence and operational performance insights.

</p>
""", unsafe_allow_html=True)
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

df["Downtime_Hours"] = (
    df["Downtime_Minutes"] / 60
).round(1)

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
<div class="gradient-heading">
📊 Dashboard Overview
</div>

<div class="section-note">
Monitor the overall status of faults and maintenance performance.
</div>

<br>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="
background:rgba(15,18,35,.8);
border:1px solid rgba(80,140,255,.35);
border-radius:20px;
padding:25px;
margin-bottom:25px;
box-shadow:0 0 18px rgba(70,120,255,.15);
">

<div style="font-size:18px;color:#A5B4FC;font-weight:600;">
🏥 Overall Health Score
</div>

<div style="font-size:56px;font-weight:800;color:white;margin-top:10px;">
{health_score}<span style="font-size:28px;color:#A5B4FC;"> /100</span>
</div>

<div style="font-size:18px;color:#A5B4FC;margin-top:8px;">
{status}
</div>

</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

cards = [

("📋 Total Faults",
 f"{len(filtered_df):,}",
 "Recorded faults",
 "#3B82F6"),

("📍 Locations",
 filtered_df["Location"].nunique(),
 "Affected locations",
 "#10B981"),

("📂 Categories",
 filtered_df["Category"].nunique(),
 "Fault categories",
 "#F59E0B"),

("🔧 Fault Types",
 filtered_df["Type"].nunique(),
 "Different fault types",
 "#8B5CF6"),

("⏱ Avg Downtime",
 f"{filtered_df['Downtime_Hours'].mean():.1f} hrs",
 "Average repair time",
 "#EF4444")

]

for col, card in zip([k1,k2,k3,k4,k5], cards):

    title,value,subtitle,accent = card

    with col:

        st.markdown(f"""
        <div class="kpi-card"
        style="--accent:{accent};">

        <div class="kpi-title">

        {title}

        </div>

        <div class="kpi-value">

        {value}

        </div>

        <div class="kpi-sub">

        {subtitle}

        </div>

        </div>
        """, unsafe_allow_html=True)
st.markdown(
    '<div class="cyber-divider"></div>',
    unsafe_allow_html=True
)
def style_chart(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white",
            size=16
        ),


        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        legend=dict(
            orientation="h",
            y=1.1
        ),

        xaxis=dict(
    showgrid=False,
    zeroline=False,
    tickangle=-20,
    tickfont=dict(size=12)
),

        yaxis=dict(
    showgrid=True,
    gridcolor="rgba(255,255,255,0.08)",
    zeroline=False,
    tickfont=dict(size=12)
),

    )

    return fig
# ==========================================
# TREND INTELLIGENCE
# ==========================================

st.markdown("""
<div class="gradient-heading">
📈 Fault Trend
</div>

<div class="section-note">
Number of faults recorded over time.
</div>

<br>
""", unsafe_allow_html=True)

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
    text="Fault Count"
)



fig_trend.update_traces(

    line=dict(width=4),

    marker=dict(size=10),

    textposition="top center"

)

style_chart(fig_trend)

st.plotly_chart(
    fig_trend,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)

st.markdown(
    '<div class="cyber-divider"></div>',
    unsafe_allow_html=True
)

# ==========================================
# DOWNTIME INTELLIGENCE
# ==========================================

st.subheader("⏱️ Downtime Analysis")

total_downtime_hours = round(
    filtered_df["Downtime_Hours"].sum(),
    1
)

location_downtime = (
    filtered_df.groupby("Location")["Downtime_Hours"]
    .sum()
    .sort_values(ascending=False)
)

category_downtime = (
    filtered_df.groupby("Category")["Downtime_Hours"]
    .sum()
    .sort_values(ascending=False)
)

fault_downtime = (
    filtered_df.groupby("Type")["Downtime_Hours"]
    .sum()
    .sort_values(ascending=False)
)

top_location = location_downtime.index[0]
top_location_hours = round(
    location_downtime.iloc[0],
    1
)

top_category = category_downtime.index[0]
top_category_hours = round(
    category_downtime.iloc[0],
    1
)

top_fault = fault_downtime.index[0]
top_fault_hours = round(
    fault_downtime.iloc[0],
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

emergency_pct = (
    emergency_count /
    len(filtered_df)
) * 100
st.markdown(f"""
<div style="
background:rgba(15,18,35,.78);
border-radius:18px;
padding:22px;
border:1px solid rgba(80,140,255,.25);
margin-bottom:25px;
">

<h3 style="margin-top:0;color:#60A5FA;">
🔍 Key Findings
</h3>

<div style="font-size:17px;line-height:2;color:white;">

📍 <b>Highest Downtime Location</b><br>
{top_location} ({top_location_hours:.1f} hrs)

<br><br>

📂 <b>Highest Downtime Category</b><br>
{top_category} ({top_category_hours:.1f} hrs)

<br><br>


🚨 <b>Emergency Faults</b><br>

{emergency_pct:.1f}% of all recorded faults

<br><br>
🔧 <b>Highest Downtime Fault</b><br>
{top_fault} ({top_fault_hours:.1f} hrs)

</div>

</div>
""", unsafe_allow_html=True)

col_dt1, col_dt2 = st.columns(2)

with col_dt1:

    st.subheader("📍 Top 10 Locations by Total Downtime (Hours)")

    fig_dt1 = px.bar(
        location_downtime.head(10).reset_index(),
        x="Location",
        y="Downtime_Hours",
        text="Downtime_Hours",
        labels={
            "Downtime_Hours": "Downtime (Hours)"
        }
    )

    fig_dt1.update_traces(
        textposition="outside",
        texttemplate="%{text:,.1f} hrs",
        marker_line_width=0
    )

    style_chart(fig_dt1)

    st.plotly_chart(
        fig_dt1,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with col_dt2:

    st.subheader("📍 Top 10 Locations by Total Downtime (Hours)")

    fig_dt2 = px.bar(
        fault_downtime.head(10).reset_index(),
        x="Type",
        y="Downtime_Hours",
        text="Downtime_Hours",
        labels={
            "Downtime_Hours": "Downtime (Hours)"
        }
    )

    fig_dt2.update_traces(
        textposition="outside",
        marker_line_width=0,
        texttemplate="%{text:,.1f} hrs"
    )

    style_chart(fig_dt2)

    st.plotly_chart(
        fig_dt2,
        use_container_width=True,
        config={"displayModeBar": False}
    )

st.markdown(
    '<div class="cyber-divider"></div>',
    unsafe_allow_html=True
)

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

risk_df["Priority"] = "🟢 Low"

risk_df.loc[
    risk_df["Risk Score"] >= risk_df["Risk Score"].quantile(0.66),
    "Priority"
] = "🔴 High"

risk_df.loc[
    (
        risk_df["Risk Score"] >= risk_df["Risk Score"].quantile(0.33)
    ) &
    (
        risk_df["Risk Score"] < risk_df["Risk Score"].quantile(0.66)
    ),
    "Priority"
] = "🟠 Medium"

st.markdown("""
<div class="gradient-heading">
⚠ Maintenance Priority
</div>

<div class="section-note">
Categories requiring the most attention.
</div>

<br>
""", unsafe_allow_html=True)

st.dataframe(

    risk_df[
        [
            "Category",
            "Fault Count",
            "Avg Downtime (hrs)",
            "Priority"
        ]
    ],

    use_container_width=True,

    hide_index=True

)

# ==========================================
# CRITICAL FAULT RADAR
# ==========================================

st.markdown(
    '<div class="cyber-divider"></div>',
    unsafe_allow_html=True
)

st.subheader("🚨 Fault Impact Analysis")

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
    text="Impact Score"
)

fig_radar.update_traces(
    textposition="outside",
    marker_line_width=0
)

style_chart(fig_radar)

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
    y="Count",
    text="Count"
    )
    
    fig.update_traces(
        textposition="outside",
        marker_line_width=0
    )
    
    style_chart(fig)
    
    st.plotly_chart(
            fig,
            use_container_width=True
        )

with col2:

    st.markdown("""
<div class="gradient-heading">
🚨 Severity Breakdown
</div>

<div class="section-note">
Distribution of faults by severity.
</div>

<br>
""", unsafe_allow_html=True)

    severity_summary = (
        filtered_df["Severity"]
        .value_counts()
        .reset_index()
    )

    severity_summary.columns = [
        "Severity",
        "Count"
    ]

    fig2 = px.pie(

        severity_summary,

        names="Severity",

        values="Count",

        hole=0.65,

        color="Severity",

        color_discrete_map={

            "Emergency": "#EF4444",
            "Urgent": "#F59E0B",
            "Normal": "#3B82F6",
            "Low": "#22C55E"

        }

    )

    fig2.update_traces(

        textposition="inside",

        textinfo="label+percent",

        textfont_size=15,

        marker=dict(

            line=dict(

                color="#111827",

                width=2

            )

        )

    )

    style_chart(fig2)

    fig2.add_annotation(

        text=f"<b>{len(filtered_df):,}</b><br>Total Faults",

        x=0.5,

        y=0.5,

        showarrow=False,

        font=dict(

            size=22,

            color="white"

        )

    )

    st.plotly_chart(

        fig2,

        use_container_width=True,

        config={"displayModeBar": False}

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
    y="Count",
    text="Count"
)

    fig3.update_traces(
    textposition="outside",
    marker_line_width=0
)

    style_chart(fig3)

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

        y="Count",

        text="Count"

    )

    fig4.update_traces(

        textposition="outside",

        marker_line_width=0

    )

    style_chart(fig4)

    st.plotly_chart(

        fig4,

        use_container_width=True,

        config={"displayModeBar": False}

    )

# ==========================================
# AI INSIGHTS
# ==========================================

st.markdown(
    '<div class="cyber-divider"></div>',
    unsafe_allow_html=True
)

st.subheader("🤖 AI Summary & Recommendations")

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

st.markdown(f"""
<div style="
background:rgba(15,18,35,.80);
border-radius:20px;
padding:25px;
border:1px solid rgba(80,140,255,.25);
">

<h2 style="color:#60A5FA;margin-top:0;">
📌 Executive Summary
</h2>

<hr style="border:1px solid rgba(255,255,255,.08);">

<h3 style="color:white;">
📍 Key Findings
</h3>

<ul style="font-size:17px;color:#D1D5DB;line-height:2;">

<li><b>{top_location}</b> recorded the highest number of faults.</li>

<li><b>{top_fault}</b> contributed the highest downtime.</li>

<li><b>{top_category}</b> has the highest calculated risk.</li>

<li><b>{emergency_pct:.1f}%</b> of recorded faults are emergency cases.</li>

</ul>

<hr style="border:1px solid rgba(255,255,255,.08);">

<h3 style="color:white;">
⚠ Priority Actions
</h3>

<ul style="font-size:17px;color:#D1D5DB;line-height:2;">

<li>Increase preventive maintenance for <b>{top_location}</b>.</li>

<li>Investigate recurring <b>{top_fault}</b> faults.</li>

<li>Prioritise maintenance for <b>{top_category}</b>.</li>

<li>Continue monitoring emergency faults weekly.</li>

</ul>

<hr style="border:1px solid rgba(255,255,255,.08);">

<h3 style="color:white;">
📊 Overall Status
</h3>

<p style="font-size:22px;color:white;">

Overall Health Score:
<b>{health_score}/100</b>

</p>

<p style="font-size:20px;color:#60A5FA;">

{status}

</p>

</div>
""", unsafe_allow_html=True)
# ==========================================
# FAULT REPORT GENERATOR
# ==========================================

st.markdown(
    '<div class="cyber-divider"></div>',
    unsafe_allow_html=True
)

st.subheader("📄 Fault Report Generator")

if st.button("Generate Fault Report"):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    report = []

    report.append(
        Paragraph(
            "Operational Fault Platform",
            styles["Title"]
        )
    )

    report.append(
        Paragraph(
            "Fault Analysis Report",
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
            "Fault Recommendations",
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
        label="📥 Download Fault Report",
        data=pdf,
        file_name="Executive_Fault_Report.pdf",
        mime="application/pdf"
    )

# ==========================================
# FAULT EXPLORER
# ==========================================

st.markdown(
    '<div class="cyber-divider"></div>',
    unsafe_allow_html=True
)

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


    
st.markdown(
    '<div class="cyber-divider"></div>',
    unsafe_allow_html=True
)

st.caption(
    "Operational Fault Analysis System | Built with Python, Streamlit & AI Analytics - by Firdaus"
)
