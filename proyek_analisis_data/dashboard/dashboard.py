import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Load dataset
df = pd.read_csv("all_data.csv")

# Pastikan kolom waktu dalam dataset bertipe datetime
df["dteday"] = pd.to_datetime(df["dteday"])

# Mengurutkan DataFrame berdasarkan tanggal
df.sort_values(by="dteday", inplace=True)
df.reset_index(drop=True, inplace=True)

# Sidebar - Filter Data
title_container = st.container()
col1, col2 = st.columns([1, 10])
with title_container:
    with col1:
        st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=60)
    with col2:
        st.title("Bike Rental Dashboard")

with st.sidebar:
    st.header("Filter Data")
    start_date, end_date = st.date_input("Rentang Waktu", [df["dteday"].min(), df["dteday"].max()])
    
# Filter dataset berdasarkan rentang tanggal
filtered_df = df[(df["dteday"] >= pd.to_datetime(start_date)) & (df["dteday"] <= pd.to_datetime(end_date))]

# Agregasi Data Harian
daily_orders_df = filtered_df.groupby("dteday").agg({"cnt_y": "sum"}).reset_index()
daily_orders_df.rename(columns={"cnt_y": "total_rentals"}, inplace=True)

# Metrics
total_orders = daily_orders_df["total_rentals"].sum()
average_orders = daily_orders_df["total_rentals"].mean()

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Rentals", value=total_orders)
with col2:
    st.metric("Average Rentals per Day", value=int(average_orders))

# Visualisasi - Line Chart Tren Harian
st.subheader("Daily Rental Trends")
fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(daily_orders_df["dteday"], daily_orders_df["total_rentals"], marker='o', linewidth=2, color="#90CAF9")
ax.set_xlabel("Date")
ax.set_ylabel("Total Rentals")
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=10, rotation=45)
st.pyplot(fig)

# Visualisasi - Bar Chart Pola Per Jam
st.subheader("Hourly Rental Patterns")
hourly_orders_df = filtered_df.groupby("hr").agg({"cnt_y": "sum"}).reset_index()
hourly_orders_df.rename(columns={"cnt_y": "total_rentals"}, inplace=True)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=hourly_orders_df["hr"], y=hourly_orders_df["total_rentals"], palette="Blues", ax=ax)
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# --- Monthly Rentals ---
monthly_rentals = df.groupby(df["dteday"].dt.strftime('%Y-%m'))["cnt_y"].sum()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_rentals.index, monthly_rentals.values, marker='o', linestyle='-', color='#42A5F5')
ax.set_title("Monthly Rentals Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Total Rentals")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# --- Weather Impact ---
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(x="weathersit_y", y="cnt_y", data=df, ax=ax, palette="coolwarm")
ax.set_title("Impact of Weather on Rentals")
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# --- User Type Comparison ---
user_type_df = df.groupby("hr")[["casual_y", "registered_y"]].sum()
fig, ax = plt.subplots(figsize=(10, 6))
user_type_df.plot(kind='bar', stacked=True, ax=ax, colormap='viridis')
ax.set_title("User Type Comparison by Hour")
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Total Users")
st.pyplot(fig)

# --- Correlation Heatmap ---
correlation_matrix = df[["temp_y", "hum_y", "windspeed_y", "cnt_y"]].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
ax.set_title("Feature Correlation Heatmap")
st.pyplot(fig)

st.write("### Dashboard Summary")
st.write("Dashboard ini menampilkan tren penyewaan sepeda berdasarkan waktu, cuaca, dan tipe pengguna.")



