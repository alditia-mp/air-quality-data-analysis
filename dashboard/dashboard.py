import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

st.set_page_config(
    page_title="Dashboard Analisis Kualitas Udara",
    page_icon="🌫️",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])
    return df

df = load_data()

st.title("🌫️ Dashboard Analisis Kualitas Udara Beijing (2013-2017)")

st.sidebar.title("🌫️ Filter Dashboard")

all_stations = sorted(df["station"].unique())
selected_stations = st.sidebar.multiselect(
    "Pilih Stasiun",
    options=all_stations,
    default=all_stations
)

filtered_df = df[df["station"].isin(selected_stations)]

st.subheader("📈 Pertanyaan 1: Tren Rata-rata PM2.5 per Bulan")

monthly_avg = filtered_df.groupby("month")["PM2.5"].mean()

fig1, ax1 = plt.subplots(figsize=(10, 5))
colors = ["#C44E52" if v == monthly_avg.max() else "#4C72B0" for v in monthly_avg.values]
ax1.bar(monthly_avg.index, monthly_avg.values, color=colors)
ax1.set_xticks(range(1, 13))
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Rata-rata PM2.5 (µg/m³)")
ax1.set_title("Rata-rata Konsentrasi PM2.5 per Bulan")
st.pyplot(fig1)

st.caption(
    "💡 **Insight:** Polusi PM2.5 cenderung memuncak pada bulan-bulan musim dingin "
    "(Desember-Maret) dan berada di titik terendah sekitar pertengahan tahun (Agustus)."
)

st.subheader("🏭 Pertanyaan 2: Perbandingan Antar Stasiun & Pengaruh Kecepatan Angin")

col1, col2 = st.columns(2)

with col1:
    station_avg = filtered_df.groupby("station")["PM2.5"].mean().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    colors2 = ["#C44E52" if v == station_avg.max() else ("#55A868" if v == station_avg.min() else "#4C72B0") for v in station_avg.values]
    ax2.barh(station_avg.index[::-1], station_avg.values[::-1], color=colors2[::-1])
    ax2.set_xlabel("Rata-rata PM2.5 (µg/m³)")
    ax2.set_title("Rata-rata PM2.5 per Stasiun")
    st.pyplot(fig2)

with col2:
    sample = filtered_df.sample(min(3000, len(filtered_df)), random_state=42)
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=sample, x="WSPM", y="PM2.5", alpha=0.3, ax=ax3)
    ax3.set_title("Kecepatan Angin (WSPM) vs PM2.5")
    st.pyplot(fig3)

corr = filtered_df["WSPM"].corr(filtered_df["PM2.5"])
st.caption(
    f"💡 **Insight:** Korelasi antara kecepatan angin dan PM2.5 pada data terfilter adalah "
    f"**{corr:.3f}**. Nilai negatif menunjukkan bahwa semakin kencang angin, semakin rendah "
    "konsentrasi PM2.5 akibat proses dispersi polutan."
)

st.subheader("🏷️ Analisis Lanjutan: Distribusi Kategori Kualitas Udara")

label_order = ["Baik", "Sedang", "Tidak Sehat", "Sangat Tidak Sehat", "Berbahaya"]
cat_counts = filtered_df["kategori_udara"].value_counts().reindex(label_order).fillna(0)

fig4, ax4 = plt.subplots(figsize=(9, 5))
colors_cat = ["#FDE2D0", "#FBBE8C", "#F28E4C", "#D9541F", "#8C2E0A"]
ax4.bar(cat_counts.index, cat_counts.values, color=colors_cat)
ax4.spines["top"].set_visible(False)
ax4.spines["right"].set_visible(False)
ax4.spines["left"].set_visible(False)
ax4.set_yticks([])
for i, v in enumerate(cat_counts.values):
    ax4.text(i, v + 3000, f"{v:,.0f}", ha="center", fontsize=10)
ax4.set_title("Distribusi Kategori Kualitas Udara (Binning PM2.5)")
st.pyplot(fig4)

st.caption(
    "💡 **Insight:** Kategori kualitas udara dibuat menggunakan teknik binning (`pd.cut`) "
    "berdasarkan standar konsentrasi PM2.5, tanpa algoritma machine learning."
)