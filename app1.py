import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set page title and icon
st.set_page_config(page_title="🚚 Delivery Data Analysis", page_icon="📦")

# Function to load dataset
@st.cache_data
def load_data():
    file_path = "delivery_data.csv"  # Ensure this file is uploaded to GitHub

    # Check if file exists
    if not os.path.exists(file_path):
        st.error("⚠️ File not found! Please upload 'delivery_data.csv' to the same folder as app.py.")
        return None

    df = pd.read_csv(file_path)

    # Strip spaces and normalize column names
    df.columns = df.columns.str.strip()

    # Debug: Show available columns
    st.write("🛠 Available Columns:", df.columns.tolist())

    # Ensure "Time_taken(min)" column exists
    if "Time_taken(min)" in df.columns:
        df["Time_taken(min)"] = df["Time_taken(min)"].astype(str).str.extract("(\d+)").astype(float)
    else:
        st.error("⚠️ Column 'Time_taken(min)' not found. Please check the dataset.")
        return None

    return df

df = load_data()

# Stop execution if file is missing
if df is None:
    st.stop()

# Sidebar Filters
st.sidebar.title("Filter Delivery Data")

# Ensure Order_Date column exists
if "Order_Date" not in df.columns:
    st.error("⚠️ Column 'Order_Date' not found in dataset. Please check your CSV file.")
    st.stop()

selected_date = st.sidebar.selectbox("Select Order Date", options=df["Order_Date"].unique())

# Ensure Road_traffic_density column exists
if "Road_traffic_density" not in df.columns:
    st.error("⚠️ Column 'Road_traffic_density' not found in dataset. Please check your CSV file.")
    st.stop()

selected_traffic = st.sidebar.multiselect("Select Traffic Density", 
                                          options=df["Road_traffic_density"].unique(), 
                                          default=df["Road_traffic_density"].unique())

# Ensure numerical operations don't fail
if df["Time_taken(min)"].dtype != float:
    st.error("⚠️ 'Time_taken(min)' column should be numeric. Please check your dataset.")
    st.stop()

min_delivery_time = st.sidebar.slider("Minimum Delivery Time (mins)", 
                                      min_value=int(df["Time_taken(min)"].min()), 
                                      max_value=int(df["Time_taken(min)"].max()), 
                                      value=int(df["Time_taken(min)"].median()))

num_records = st.sidebar.slider("Number of Records to Display", min_value=1, max_value=50, value=10)

# Filter Data
filtered_data = df[(df["Order_Date"] == selected_date) & 
                   (df["Time_taken(min)"] >= min_delivery_time) & 
                   (df["Road_traffic_density"].isin(selected_traffic))]

filtered_data = filtered_data.head(num_records)

# Display Filtered Data
st.title("🚚 Delivery Data Analysis App")
st.write(f"**Filtered Results for Date {selected_date} with Min Delivery Time {min_delivery_time} mins:**")
st.dataframe(filtered_data)

# Create Tabs for Visualization
tabs = st.tabs(["Delivery Time Distribution", "Traffic Impact on Delivery"])

with tabs[0]:
    st.subheader("📊 Delivery Time Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered_data["Time_taken(min)"], bins=10, color='blue', alpha=0.7)
    ax.set_xlabel("Time Taken (mins)")
    ax.set_ylabel("Number of Deliveries")
    ax.set_title("Distribution of Delivery Time")
    st.pyplot(fig)

with tabs[1]:
    st.subheader("🚦 Traffic Density vs Delivery Time")
    traffic_summary = filtered_data.groupby("Road_traffic_density")["Time_taken(min)"].mean().reset_index()
    fig2, ax2 = plt.subplots()
    ax2.bar(traffic_summary["Road_traffic_density"], traffic_summary["Time_taken(min)"], color='red')
    ax2.set_xlabel("Traffic Density")
    ax2.set_ylabel("Avg. Delivery Time (mins)")
    ax2.set_title("Impact of Traffic on Delivery Time")
    st.pyplot(fig2)

# Footer
st.write("🚀 Analyzing delivery data made easy!")





