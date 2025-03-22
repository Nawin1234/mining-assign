import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    file_path = "delivery_data.csv"  # Ensure this file is uploaded in GitHub

    try:
        df = pd.read_csv(file_path)
        df["Time_taken(min)"] = df["Time_taken(min)"].str.extract("(\d+)").astype(float)  # Clean time column
        return df
    except FileNotFoundError:
        st.error("⚠️ File not found! Please upload 'delivery_data.csv' to your GitHub repository.")
        return None

df = load_data()

# Stop execution if file is missing
if df is None:
    st.stop()

# Set page title and icon
st.set_page_config(page_title="Delivery Data Analysis", page_icon="🚚")

# Sidebar for user input
st.sidebar.title("Filter Delivery Data")

# Filter for order date
selected_date = st.sidebar.selectbox("Select Order Date", options=df["Order_Date"].unique())

# Slider for minimum delivery time
min_delivery_time = st.sidebar.slider("Minimum Delivery Time (mins)", 
                                      min_value=int(df["Time_taken(min)"].min()), 
                                      max_value=int(df["Time_taken(min)"].max()), 
                                      value=int(df["Time_taken(min)"].median()))

# Multi-select for traffic density
selected_traffic = st.sidebar.multiselect("Select Traffic Density", 
                                          options=df["Road_traffic_density"].unique(), 
                                          default=df["Road_traffic_density"].unique())

# Filter data based on user input
filtered_data = df[(df["Order_Date"] == selected_date) & 
                   (df["Time_taken(min)"] >= min_delivery_time) & 
                   (df["Road_traffic_density"].isin(selected_traffic))]

# Limit number of records displayed
num_records = st.sidebar.slider("Number of Records to Display", min_value=1, max_value=50, value=10)
filtered_data = filtered_data.head(num_records)

# Main title
st.title("🚚 Delivery Data Analysis App")

# Display filtered results
st.write(f"**Filtered Results for Date {selected_date} with Min Delivery Time {min_delivery_time} mins:**")
st.dataframe(filtered_data)

# Create tabs for different visualizations
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



