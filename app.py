import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Configure the Streamlit page
st.set_page_config(page_title="UrbanPulse Dashboard", layout="wide")

# ----------------------- Helper Functions -----------------------

@st.cache_data(ttl=60)
def generate_real_time_data(num_points=100, interval_minutes=5):
    """
    Generate simulated real-time urban data for traffic density and air quality.
    """
    now = datetime.now()
    time_series = [now - timedelta(minutes=interval_minutes * i) for i in range(num_points)]
    time_series = sorted(time_series)  # Ensure the list is in chronological order

    traffic_density = np.clip(np.random.normal(loc=50, scale=10, size=num_points), 20, 100)
    air_quality = np.clip(np.random.normal(loc=35, scale=8, size=num_points), 10, 80)

    df = pd.DataFrame({
        "Time": time_series,
        "Traffic Density (vehicles/min)": traffic_density,
        "PM2.5 (µg/m³)": air_quality
    })
    return df

def generate_prediction_data(latest_value, steps=12, interval_minutes=5, trend_factor=1.05):
    """
    Generate prediction data for the next period using a simple exponential trend.
    """
    last_time = datetime.now()
    future_times = [last_time + timedelta(minutes=interval_minutes * i) for i in range(1, steps + 1)]
    predicted_values = latest_value * (trend_factor ** np.arange(1, steps + 1))
    return pd.DataFrame({
        "Time": future_times,
        "Predicted Value": predicted_values
    })

def plot_line_chart(df, x, y, title, y_label=None):
    """
    Create and display a line chart using Plotly.
    """
    fig = px.line(df, x=x, y=y, title=title)
    if y_label:
        fig.update_layout(yaxis_title=y_label)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------- Main App Layout -----------------------

st.title("UrbanPulse – AI-Powered Urban Infrastructure Dashboard")

# Create tabs for the main sections
tabs = st.tabs(["Real-Time Data", "Predictive Analytics", "Simulation & Scenario Planning"])

# ----------------------- TAB 1: Real-Time Data -----------------------
with tabs[0]:
    st.header("Real-Time Urban Data Overview")

    # Generate or load simulated real-time data
    df_rt = generate_real_time_data()

    # Display a snapshot of the real-time data
    st.dataframe(df_rt.head(), use_container_width=True)

    # Use columns for side-by-side charts
    col1, col2 = st.columns(2)

    with col1:
        plot_line_chart(df_rt, x="Time", y="Traffic Density (vehicles/min)",
                        title="Live Traffic Density", y_label="Vehicles per Minute")

    with col2:
        plot_line_chart(df_rt, x="Time", y="PM2.5 (µg/m³)",
                        title="Live Air Quality (PM2.5)", y_label="µg/m³")

# ----------------------- TAB 2: Predictive Analytics -----------------------
with tabs[1]:
    st.header("Predictive Analytics")

    st.write("Forecasting upcoming urban conditions based on current trends...")

    # Predictions for Traffic Density
    latest_traffic = df_rt["Traffic Density (vehicles/min)"].iloc[-1]
    df_pred_traffic = generate_prediction_data(latest_value=latest_traffic)

    st.subheader("Traffic Density Forecast (Next Hour)")
    st.dataframe(df_pred_traffic, use_container_width=True)
    plot_line_chart(df_pred_traffic, x="Time", y="Predicted Value",
                    title="Predicted Traffic Density", y_label="Vehicles per Minute")

    # Predictions for Air Quality
    latest_pm25 = df_rt["PM2.5 (µg/m³)"].iloc[-1]
    df_pred_air = generate_prediction_data(latest_value=latest_pm25)

    st.subheader("Air Quality Forecast (PM2.5 for Next Hour)")
    st.dataframe(df_pred_air, use_container_width=True)
    plot_line_chart(df_pred_air, x="Time", y="Predicted Value",
                    title="Predicted PM2.5 Levels", y_label="µg/m³")

# ----------------------- TAB 3: Simulation & Scenario Planning -----------------------
with tabs[2]:
    st.header("Simulation & Scenario Planning")
    st.write("Test urban interventions and visualize potential impacts.")

    # Simulation: Adjust Traffic Signal Timing
    st.subheader("Traffic Signal Timing Adjustment")
    timing_adjustment = st.slider("Adjust Traffic Signal Cycle (seconds)",
                                  min_value=30, max_value=120, value=60, step=5,
                                  help="Adjust the cycle time; shorter cycles can improve flow.")

    # Assume a simple inverse relationship: lower cycle time reduces congestion
    df_sim = df_rt.copy()
    df_sim["Simulated Traffic Density"] = df_sim["Traffic Density (vehicles/min)"] * (60 / timing_adjustment)
    plot_line_chart(df_sim, x="Time", y="Simulated Traffic Density",
                    title="Simulated Traffic Density with Adjusted Signal Timing",
                    y_label="Vehicles per Minute")

    # Simulation: Impact of Green Zones on Air Quality
    st.subheader("Green Zones Impact on Air Quality")
    green_zone_effect = st.slider("Green Zone Effectiveness (%)", min_value=0, max_value=50,
                                  value=10, step=5,
                                  help="Estimated reduction in PM2.5 levels due to increased green cover.")
    
    # Calculate the simulated PM2.5 reduction
    df_sim["Simulated PM2.5"] = df_sim["PM2.5 (µg/m³)"] * (1 - green_zone_effect / 100)
    plot_line_chart(df_sim, x="Time", y="Simulated PM2.5",
                    title="Simulated Air Quality with Enhanced Green Zones",
                    y_label="µg/m³")

    st.success("Simulation complete. Experiment with different parameters to plan effective urban interventions.")
