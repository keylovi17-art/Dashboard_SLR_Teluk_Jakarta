import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ==========================================
# KONFIGURASI DAN PEMBACAAN DATA
# ==========================================

st.set_page_config(
    page_title="Historis SLA - Teluk Jakarta",
    page_icon="🌊",
    layout="wide"
)

# ==========================================
# HEADER GLOBAL DASHBOARD
# ==========================================

st.markdown("""
<style>
.header-dashboard {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 95px;
    z-index: 999999;
    background-color: #253E51;
    padding: 16px 30px;
    box-sizing: border-box;
    margin: 0;
}

.header-dashboard h1 {
    color: white;
    font-size: 30px;
    font-weight: 700;
    margin: 0;
    padding: 0;
}

.header-dashboard p {
    color: #CBDAE6;
    font-size: 14px;
    margin: 4px 0 0 0;
}

/* Memberi ruang untuk header tetap */
[data-testid="stAppViewContainer"] {
    padding-top: 110px;
}
</style>

<div class="header-dashboard">
    <h1>SEA LEVEL RISE DASHBOARD</h1>
    <p>Analisis Historis dan Proyeksi Kenaikan Muka Laut di Teluk Jakarta</p>
</div>
""", unsafe_allow_html=True)


DATA_PATH = os.path.join(
    "data",
    "Data_Historis_SLA_Dashboard_AR1.csv"
)

df = pd.read_csv(DATA_PATH)
df["tanggal"] = pd.to_datetime(df["tanggal"])

# ==========================================
# JUDUL HALAMAN
# ==========================================

st.title("Analisis Historis Sea Level Anomaly")
st.markdown("""
Halaman ini menyajikan perubahan **Sea Level Anomaly (SLA)**
di perairan Teluk Jakarta berdasarkan data satelit altimetri
periode 1993–2025.
""")

st.divider()

# ==========================================
# RINGKASAN HASIL
# ==========================================

st.subheader("Ringkasan Hasil Pengolahan")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tren Historis", "4,231 mm/tahun")

with col2:
    st.metric("Periode Pengamatan", "1993–2025")

with col3:
    st.metric("Jumlah Observasi", f"{len(df)} bulan")

st.caption(
    "Tren dihitung menggunakan model SARIMAX "
    "dengan komponen autoregresif AR(1)."
)

st.divider()

# ==========================================
# FILTER PERIODE
# ==========================================

st.subheader("Grafik Perubahan SLA Historis")

tahun_min = int(df["tanggal"].dt.year.min())
tahun_max = int(df["tanggal"].dt.year.max())

rentang_tahun = st.slider(
    "Pilih rentang tahun pengamatan",
    min_value=tahun_min,
    max_value=tahun_max,
    value=(tahun_min, tahun_max)
)

df_filter = df[
    (df["tanggal"].dt.year >= rentang_tahun[0]) &
    (df["tanggal"].dt.year <= rentang_tahun[1])
]

# ==========================================
# GRAFIK SLA DAN FITTED SARIMAX
# ==========================================

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_filter["tanggal"],
    y=df_filter["SLA_Rata_Rata"] * 1000,
    mode="lines",
    name="SLA Aktual",
    line=dict(color="#416E8B", width=1.5)
))

fig.add_trace(go.Scatter(
    x=df_filter["tanggal"],
    y=df_filter["Fitted_SARIMAX"] * 1000,
    mode="lines",
    name="Fitted SARIMAX AR(1)",
    line=dict(color="#19293B", width=2)
))

fig.update_layout(
    title="Perubahan Sea Level Anomaly (SLA) Historis",
    xaxis_title="Tahun",
    yaxis_title="SLA (mm)",
    hovermode="x unified",
    template="plotly_white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=20, r=20, t=70, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Garis SLA Aktual menunjukkan data pengamatan, sedangkan "
    "Fitted SARIMAX AR(1) menunjukkan hasil estimasi model "
    "satu langkah ke depan."
)

st.divider()

# ==========================================
# INTERPRETASI SEMENTARA
# ==========================================

st.subheader("Interpretasi Hasil")

st.info("""
**Interpretasi sementara**

Hasil pengolahan menunjukkan tren historis SLA sebesar
4,231 mm/tahun berdasarkan model SARIMAX AR(1).

Nilai tersebut menggambarkan kecenderungan perubahan SLA
selama periode pengamatan 1993–2025. Grafik memperlihatkan
perbandingan antara data SLA aktual dan nilai estimasi model.

Pembahasan lebih lanjut mengenai pola temporal dan faktor
yang memengaruhi perubahan SLA akan dilengkapi berdasarkan
kajian literatur.
""")

# ==========================================
# INFORMASI SUMBER DATA
# ==========================================

st.subheader("Sumber Data dan Metode")

st.markdown("""
- **Sumber data:** Copernicus Marine Service.
- **Jenis data:** Sea Level Anomaly (SLA) dari satelit altimetri.
- **Periode:** Januari 1993–Desember 2025.
- **Jumlah observasi:** 396 data bulanan.
- **Metode analisis:** SARIMAX(1,0,0) dengan variabel tren
  dan dummy bulanan.
- **Pengolahan:** Python, Pandas, dan Statsmodels.
""")
