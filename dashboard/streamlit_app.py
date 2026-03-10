import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Smart Farming Dashboard", layout="wide")

st.markdown("""
<style>

.main {
    background-color: #f5f9ff;
}

h1, h2, h3 {
    color: #1f4e79;
}

div[data-testid="stMetric"] {
    background-color: #e8f1ff;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #1f77b4;
}

div[data-testid="stMetric"] label {
    color: black !important;
}

div[data-testid="stMetric"] div {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

df = pd.read_csv("../outputs/cleaned_data.csv")

st.title("🌱 Smart Farming Soil Monitoring Dashboard")

st.sidebar.title("🔎 Hi, Welcome!")

st.sidebar.write("""
Dashboard ini menampilkan data **kelembaban tanah dari beberapa sensor**
yang digunakan dalam sistem **Smart Farming berbasis IoT**.

Gunakan filter untuk menganalisis kondisi tanah berdasarkan sensor dan waktu.
""")

sensor_options = {
    "Soil Sensor 1": "moisture0",
    "Soil Sensor 2": "moisture1",
    "Soil Sensor 3": "moisture2",
    "Soil Sensor 4": "moisture3",
    "Soil Sensor 5": "moisture4"
}

selected_sensor_name = st.sidebar.selectbox(
    "Pilih Sensor Tanah",
    list(sensor_options.keys())
)

sensor = sensor_options[selected_sensor_name]

selected_month = st.sidebar.selectbox(
    "Pilih Bulan",
    sorted(df["month"].unique())
)

selected_hour = st.sidebar.slider(
    "Filter Jam",
    int(df["hour"].min()),
    int(df["hour"].max()),
    (int(df["hour"].min()), int(df["hour"].max()))
)

df_filtered = df[
    (df["month"] == selected_month) &
    (df["hour"] >= selected_hour[0]) &
    (df["hour"] <= selected_hour[1])
]

st.subheader("📊 Current Sensor Status")

col1, col2, col3 = st.columns(3)

current = df_filtered[sensor].iloc[-1]
avg = df_filtered[sensor].mean()
max_val = df_filtered[sensor].max()

col1.metric("Current Moisture", round(current,2))
col2.metric("Average Moisture", round(avg,2))
col3.metric("Max Moisture", round(max_val,2))

st.subheader(f"📈 Soil Moisture Trend - {selected_sensor_name}")

fig, ax = plt.subplots()

ax.plot(df_filtered[sensor], color="#1f77b4", linewidth=2)

ax.set_ylabel("Moisture Level")
ax.set_xlabel("Data Index")

st.pyplot(fig)

col4, col5 = st.columns(2)

with col4:
    st.subheader("📊 Moisture Distribution")

    fig2, ax2 = plt.subplots()

    ax2.hist(df_filtered[sensor], bins=20, color="#4da6ff")

    st.pyplot(fig2)

with col5:
    st.subheader("🔥 Sensor Correlation")

    fig3, ax3 = plt.subplots()

    sns.heatmap(
        df[['moisture0','moisture1','moisture2','moisture3','moisture4']].corr(),
        annot=True,
        cmap="Blues",
        ax=ax3
    )

    st.pyplot(fig3)

st.subheader("💧 Irrigation Activity")

fig4, ax4 = plt.subplots()

df['irrgation'].value_counts().plot(
    kind='bar',
    color=["#4da6ff","#1f77b4"],
    ax=ax4
)

ax4.set_xlabel("Irrigation Status")
ax4.set_ylabel("Count")

st.pyplot(fig4)

st.subheader("🚨 Soil Moisture Status")

if current < 30:
    st.error("⚠ Soil Too Dry - Irrigation Needed")
else:
    st.success("✅ Soil Moisture Normal")
