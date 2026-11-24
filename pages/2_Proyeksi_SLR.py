
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Proyeksi SLR - Teluk Jakarta",
    page_icon="🌊",
    layout="wide"
)

# ==========================================
# HEADER GLOBAL
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

[data-testid="stAppViewContainer"] {
    padding-top: 110px;
}
</style>

<div class="header-dashboard">
    <h1>SEA LEVEL RISE DASHBOARD</h1>
    <p>Analisis Historis dan Proyeksi Kenaikan Muka Laut di Teluk Jakarta</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MEMBACA DATA
# ==========================================

DATA_PATH = os.path.join(
    "data",
    "Proyeksi_AR6_2035_2045.csv"
)

df = pd.read_csv(DATA_PATH)

# ==========================================
# JUDUL DAN DESKRIPSI
# ==========================================

st.title("Proyeksi Kenaikan Muka Laut IPCC AR6")

st.markdown("""
Halaman ini menyajikan proyeksi perubahan muka laut di wilayah
kajian berdasarkan skenario iklim **SSP2-4.5** dan **SSP5-8.5**
dari IPCC AR6 untuk tahun 2035 dan 2045.
""")

st.divider()

# ==========================================
# FILTER PROYEKSI
# ==========================================

st.subheader("Pengaturan Proyeksi")

col1, col2 = st.columns(2)

with col1:
    skenario = st.selectbox(
        "Pilih skenario iklim",
        sorted(df["Skenario"].unique())
    )

with col2:
    kuantil = st.selectbox(
        "Pilih tingkat kuantil",
        ["P5", "P50", "P95"],
        index=1
    )

df_filter = df[
    (df["Skenario"] == skenario) &
    (df["Kuantil"] == kuantil)
].sort_values("Tahun")

# ==========================================
# RINGKASAN NILAI
# ==========================================

st.divider()
st.subheader("Ringkasan Nilai Proyeksi")

col1, col2 = st.columns(2)

for col, tahun in zip([col1, col2], [2035, 2045]):
    nilai = df_filter.loc[
        df_filter["Tahun"] == tahun,
        "Proyeksi_mm"
    ]

    with col:
        if not nilai.empty:
            st.metric(
                label=f"Proyeksi Tahun {tahun}",
                value=f"{nilai.iloc[0]:,.1f} mm"
            )

st.caption(
    f"Nilai proyeksi untuk skenario {skenario} "
    f"pada tingkat kuantil {kuantil}."
)

# ==========================================
# GRAFIK PROYEKSI
# ==========================================

st.divider()
st.subheader("Grafik Proyeksi Muka Laut")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_filter["Tahun"],
    y=df_filter["Proyeksi_mm"],
    mode="lines+markers+text",
    text=df_filter["Proyeksi_mm"].map(
        lambda x: f"{x:.1f} mm"
    ),
    textposition="top center",
    name=f"{skenario} - {kuantil}",
    line=dict(color="#416E8B", width=3),
    marker=dict(size=10, color="#253E51")
))

fig.update_layout(
    title=f"Proyeksi Muka Laut: {skenario} ({kuantil})",
    xaxis_title="Tahun",
    yaxis_title="Proyeksi (mm)",
    template="plotly_white",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# INTERPRETASI SEMENTARA
# ==========================================

st.divider()
st.subheader("Interpretasi Hasil")

st.info(f"""
**Interpretasi sementara**

Pada skenario {skenario} dengan kuantil {kuantil},
nilai proyeksi muka laut yang ditampilkan merupakan estimasi
untuk tahun 2035 dan 2045 berdasarkan data IPCC AR6.

Nilai P50 menunjukkan median proyeksi, sedangkan P5 dan P95
menunjukkan kuantil bawah dan atas dari distribusi proyeksi.

Pembahasan lebih lanjut akan dilengkapi berdasarkan kajian
literatur dan interpretasi hasil penelitian.
""")

# ==========================================
# SUMBER DATA
# ==========================================

st.divider()
st.subheader("Sumber Data dan Metode")

st.markdown("""
- **Sumber:** IPCC Sixth Assessment Report (AR6).
- **Skenario:** SSP2-4.5 dan SSP5-8.5.
- **Tahun proyeksi:** 2035 dan 2045.
- **Tingkat kuantil:** P5, P50, dan P95.
- **Pengolahan:** Python dan Pandas.
- **Visualisasi:** Plotly dan Streamlit.
""")

st.warning("""
Data proyeksi menggunakan grid regional terdekat dengan wilayah
kajian, bukan pengukuran langsung di garis pantai Tanjung Priok.
Data ini juga tidak memasukkan penurunan muka tanah lokal.
""")
