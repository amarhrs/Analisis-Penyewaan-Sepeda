import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Muat Data
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# Gabungkan Data
combined_df = pd.merge(day_df, hour_df, on='dteday', suffixes=('_day', '_hour'))

# Judul Dashboard
st.title("Dashboard Analisis Penyewaan Sepeda")

# Sidebar untuk Filter
with st.sidebar:
    st.sidebar.header("Filter Data")
    selected_season = st.sidebar.selectbox('Pilih Musim', (1, 2, 3, 4), format_func=lambda x: ['Spring', 'Summer', 'Fall', 'Winter'][x-1])
    selected_workingday = st.sidebar.radio("Hari Kerja atau Hari Libur?", (0, 1), format_func=lambda x: 'Libur/Akhir Pekan' if x == 0 else 'Hari Kerja')

# Filter Data berdasarkan Input User
filtered_df = combined_df[(combined_df['season_day'] == selected_season) & (combined_df['workingday_hour'] == selected_workingday)]
print(filtered_df.columns)

# Tampilan Data
st.subheader(f"Data Penyewaan Sepeda untuk Musim {'Spring' if selected_season == 1 else 'Summer' if selected_season == 2 else 'Fall' if selected_season == 3 else 'Winter'} pada {'Libur/Akhir Pekan' if selected_workingday == 0 else 'Hari Kerja'}")
st.write(filtered_df)

# Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca
weather_avg = filtered_df.groupby("weathersit_hour")["cnt_hour"].mean()
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
st.bar_chart(weather_avg)

# Rata-rata Penyewaan Sepeda Berdasarkan Jam
hourly_avg = filtered_df.groupby("hr")["cnt_hour"].mean()
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Jam")
st.line_chart(hourly_avg)

# Korelasi Antar Variabel
correlation = filtered_df[['cnt_day', 'cnt_hour', 'temp_hour', 'atemp_hour', 'hum_hour', 'windspeed_hour']].corr()
fig, ax = plt.subplots()
st.subheader("Korelasi Antar Variabel")
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Grafik Tren Penyewaan Sepeda
st.subheader("Tren Penyewaan Sepeda Sepanjang Waktu")
combined_df['dteday'] = pd.to_datetime(combined_df['dteday'])
combined_df.set_index('dteday', inplace=True)
monthly_avg = combined_df['cnt_hour'].resample('M').mean()
st.line_chart(monthly_avg)