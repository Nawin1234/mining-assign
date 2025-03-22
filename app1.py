import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    file_path = "./delivery_data.csv"  # Ensure correct path

   # Ensure this file is uploaded in GitHub

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

# Streamlit UI
st.title("📦 Amazon-Style Delivery Analytics")

# Sidebar filters
st.sidebar.header("Filter Options")
city = st.sidebar.selectbox("Select City", ["All"] + list(df["City"].unique()))
vehicle = st.sidebar.selectbox("Select Vehicle Type", ["All"] + list(df["Type_of_vehicle"].unique()))

# Apply filters
if city != "All":
    df = df[df["City"] == city]
if vehicle != "All":
    df = df[df["Type_of_vehicle"] == vehicle]

# Show Data
st.subheader("📊 Data Preview")
st.dataframe(df.head())

# Visualization - Delivery Time Distribution
st.subheader("⏳ Delivery Time Analysis")
fig, ax = plt.subplots()
sns.histplot(df["Time_taken(min)"], bins=20, kde=True, ax=ax)
st.pyplot(fig)

st.subheader("🚦 Traffic Density Impact")
traffic_group = df.groupby("Road_traffic_density")["Time_taken(min)"].mean()
st.bar_chart(traffic_group)

st.subheader("🌦️ Weather Impact on Delivery Time")
weather_group = df.groupby("Weatherconditions")["Time_taken(min)"].mean()
st.bar_chart(weather_group)

st.write("📊 Use the sidebar to filter data dynamically!")


