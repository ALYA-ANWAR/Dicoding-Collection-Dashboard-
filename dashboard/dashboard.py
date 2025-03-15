import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Load data dengan pengecekan keberadaan file
file_path = "dashboard/all_data.csv"
if not os.path.exists(file_path):
    st.error(f"Dataset tidak ditemukan di lokasi: {file_path}. Pastikan path sudah benar.")
    st.stop()

df = pd.read_csv(file_path)
df["dteday"] = pd.to_datetime(df["dteday"])

# Pastikan kolom yang dibutuhkan tersedia
required_columns = {"season_x", "hr", "workingday_x", "cnt_x", "dteday"}
missing_columns = required_columns - set(df.columns)
if missing_columns:
    st.error(f"Kolom berikut tidak ditemukan dalam dataset: {missing_columns}")
    st.stop()

# Mapping musim
season_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
df["season_x"] = df["season_x"].map(season_mapping)

# Judul Dashboard
st.title("Dashboard Peminjaman Sepeda 🚴✨")

# Sidebar - Fitur Interaktif
st.sidebar.header("Filter Data")
st.sidebar.image("dashboard/sepedaa.jpg")

# Pilihan musim dengan opsi "All Season"
season_options = ["All Season"] + list(df["season_x"].dropna().unique())
selected_season = st.sidebar.selectbox("Pilih Musim", season_options)

# Filter rentang tanggal
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal", [df["dteday"].min(), df["dteday"].max()],
    min_value=df["dteday"].min(), max_value=df["dteday"].max()
)

# Filter data berdasarkan rentang tanggal saja (untuk grafik pertama)
filtered_df_date = df[(df["dteday"] >= pd.to_datetime(start_date)) & (df["dteday"] <= pd.to_datetime(end_date))]

# Filter data berdasarkan musim saja (untuk grafik kedua)
if selected_season == "All Season":
    filtered_df_season = df.copy()
else:
    filtered_df_season = df[df["season_x"] == selected_season]

# Grafik 1: Pola Penggunaan Sepeda (Hanya berdasarkan tanggal, tidak terpengaruh musim)
st.subheader("Pola Penggunaan Sepeda: Hari Kerja vs Akhir Pekan")
time_usage = filtered_df_date.groupby(["hr", "workingday_x"]).agg({"cnt_x": "sum"}).reset_index()

weekday_usage = time_usage[time_usage["workingday_x"] == 1]
weekend_usage = time_usage[time_usage["workingday_x"] == 0]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(weekday_usage["hr"], weekday_usage["cnt_x"], marker='o', label="Hari Kerja", color="blue")
ax.plot(weekend_usage["hr"], weekend_usage["cnt_x"], marker='o', label="Akhir Pekan", color="red")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Peminjaman Sepeda per Jam")
ax.legend()
ax.grid()
st.pyplot(fig)

# Grafik 2: Pengaruh Musim terhadap Peminjaman Sepeda (Hanya berdasarkan musim, tidak terpengaruh tanggal)
st.subheader("Pengaruh Musim terhadap Peminjaman Sepeda")
seasonal_usage = filtered_df_season.groupby("season_x").agg({"cnt_x": "sum"}).reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season_x", y="cnt_x", hue="season_x", data=seasonal_usage, dodge=False, legend=False, ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Total Peminjaman Sepeda Berdasarkan Musim")
st.pyplot(fig)

st.write("### Dashboard ini menampilkan pola peminjaman sepeda berdasarkan jam serta pengaruh musim terhadap jumlah peminjaman.")
