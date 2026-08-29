"""Desktop CPU Status & System Monitoring Dashboard using Streamlit."""
import os
import sys
import time
from typing import List
import pandas as pd
import streamlit as st

# Import metrics service
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from metrics import SystemMetricsService

# Check if plotly is available
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


# Page Configuration
st.set_page_config(
    page_title="Desktop CPU Status Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-metric-card {
        background-color: #1E1E2E;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #313244;
        text-align: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #89B4FA;
    }
    .metric-label {
        font-size: 14px;
        color: #A6ADC8;
    }
    .stProgress > div > div > div > div {
        background-color: #89B4FA;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State for Historical Time-Series Data
if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = []
if "time_history" not in st.session_state:
    st.session_state.time_history = []


# Sidebar Controls
st.sidebar.title("⚙️ Dashboard Controls")

refresh_rate = st.sidebar.slider("⏱️ Refresh Interval (seconds)", min_value=0.5, max_value=5.0, value=1.0, step=0.5)
auto_refresh = st.sidebar.toggle("🔄 Auto Refresh", value=True)
alert_threshold = st.sidebar.slider("🚨 High CPU Alert Threshold (%)", min_value=50, max_value=95, value=80, step=5)
max_history_points = st.sidebar.slider("📈 Max History Points", min_value=20, max_value=120, value=60, step=10)

st.sidebar.divider()
st.sidebar.subheader("🔍 Process Filters")
proc_limit = st.sidebar.slider("Top Processes Count", min_value=5, max_value=30, value=10, step=5)
proc_search = st.sidebar.text_input("Filter Process by Name", "")
proc_sort = st.sidebar.selectbox("Sort Processes By", ["CPU (%)", "RAM (%)"], index=0)

if st.sidebar.button("🧹 Clear History"):
    st.session_state.cpu_history = []
    st.session_state.time_history = []
    st.sidebar.success("History cleared!")


# Fetch System Metrics
cpu_data = SystemMetricsService.get_cpu_summary()
mem_data = SystemMetricsService.get_memory_summary()
sys_info = SystemMetricsService.get_system_info()
sort_key = "cpu_percent" if proc_sort == "CPU (%)" else "memory_percent"
processes = SystemMetricsService.get_top_processes(limit=proc_limit, search=proc_search, sort_by=sort_key)

# Update History
current_time_str = time.strftime("%H:%M:%S")
st.session_state.cpu_history.append(cpu_data["overall_percent"])
st.session_state.time_history.append(current_time_str)

if len(st.session_state.cpu_history) > max_history_points:
    st.session_state.cpu_history.pop(0)
    st.session_state.time_history.pop(0)


# Title & System Info Header
st.title("⚡ Desktop CPU & System Status")
st.caption(
    f"🖥️ **Host:** `{sys_info['node']}` | **OS:** `{sys_info['system']} {sys_info['release']}` | "
    f"**Processor:** `{sys_info['machine']}` | **Uptime:** `{sys_info['uptime']}` | **Booted:** `{sys_info['boot_time']}`"
)

# High CPU Alert
if cpu_data["overall_percent"] >= alert_threshold:
    st.error(f"🚨 **High CPU Usage Alert:** Overall CPU utilization is currently at **{cpu_data['overall_percent']}%** (Exceeds {alert_threshold}% threshold)!")


# High-Level Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Overall CPU Usage",
        value=f"{cpu_data['overall_percent']}%",
        delta=f"{round(cpu_data['overall_percent'] - (st.session_state.cpu_history[-2] if len(st.session_state.cpu_history) > 1 else cpu_data['overall_percent']), 1)}%",
    )

with col2:
    st.metric(
        label="RAM Utilization",
        value=f"{mem_data['ram']['percent']}%",
        help=f"{mem_data['ram']['used_gb']} GB / {mem_data['ram']['total_gb']} GB",
    )

with col3:
    st.metric(
        label="Cores (Phys / Log)",
        value=f"{cpu_data['physical_cores']} / {cpu_data['logical_cores']}",
    )

with col4:
    freq_val = f"{cpu_data['frequency']['current']} MHz" if cpu_data['frequency']['current'] != "N/A" else "Dynamic"
    st.metric(
        label="CPU Frequency",
        value=freq_val,
    )

with col5:
    load_val = f"{cpu_data['load_avg'].get('1min', '-')}, {cpu_data['load_avg'].get('5min', '-')}"
    st.metric(
        label="Load Avg (1m, 5m)",
        value=load_val,
    )

st.divider()


# Main Visuals: Timeline & Per-Core Usage
chart_col, core_col = st.columns([3, 2])

with chart_col:
    st.subheader("📈 Real-time CPU Usage Timeline")
    if len(st.session_state.cpu_history) > 0:
        history_df = pd.DataFrame({
            "Time": st.session_state.time_history,
            "CPU (%)": st.session_state.cpu_history,
        })
        if PLOTLY_AVAILABLE:
            fig = px.area(
                history_df,
                x="Time",
                y="CPU (%)",
                title="Overall CPU % Over Time",
                color_discrete_sequence=["#89B4FA"],
            )
            fig.update_layout(
                yaxis_range=[0, 100],
                margin=dict(l=20, r=20, t=30, b=20),
                height=300,
                template="plotly_dark",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.line_chart(history_df.set_index("Time"), height=300)

with core_col:
    st.subheader("🧩 Per-Core Utilization")
    per_core = cpu_data["per_core"]
    core_cols = st.columns(2)
    for idx, usage in enumerate(per_core):
        with core_cols[idx % 2]:
            st.write(f"**Core {idx}**: `{usage}%`")
            st.progress(min(int(usage), 100) / 100.0)


st.divider()


# Memory Breakdown & Top Processes
mem_col, proc_col = st.columns([1, 2])

with mem_col:
    st.subheader("💾 Memory Breakdown")
    st.write(f"**RAM Usage**: `{mem_data['ram']['used_gb']} GB` / `{mem_data['ram']['total_gb']} GB` (`{mem_data['ram']['percent']}%`)")
    st.progress(mem_data['ram']['percent'] / 100.0)
    st.caption(f"Available: `{mem_data['ram']['available_gb']} GB`")

    st.write(f"**Swap Usage**: `{mem_data['swap']['used_gb']} GB` / `{mem_data['swap']['total_gb']} GB` (`{mem_data['swap']['percent']}%`)")
    st.progress(mem_data['swap']['percent'] / 100.0)
    st.caption(f"Free: `{mem_data['swap']['free_gb']} GB`")

with proc_col:
    st.subheader(f"📊 Top {proc_limit} Resource-Consuming Processes")
    if processes:
        proc_df = pd.DataFrame(processes)
        st.dataframe(
            proc_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No matching processes found.")


# Auto-refresh loop
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
