import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Perbandingan Proyeksi - Teluk Jakarta",
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
}

.header-dashboard h1 {
    color: white;
    font-size: 30px;
    margin: 0;
    padding: 0;
    line-height: 1.3;
}

.header-dashboard p {
    color: #CBDAE6;
    font-size: 14px;
    margin: 4px 0 0 0;
    line-height: 1.3;
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
# JUDUL HALAMAN
# ==========================================

st.title("Perbandingan Skenario Proyeksi")

st.markdown("""
Halaman ini membandingkan proyeksi perubahan muka laut
berdasarkan dua skenario iklim IPCC AR6, yaitu SSP2-4.5
dan SSP5-8.5.
""")

st.divider()

# ==========================================
# PILIH KUANTIL
# ==========================================

st.subheader("Pengaturan Perbandingan")

kuantil = st.selectbox(
    "Pilih tingkat kuantil",
    ["P5", "P50", "P95"],
    index=1
)

df_filter = df[
    df["Kuantil"] == kuantil
].copy()

# ==========================================
# GRAFIK PERBANDINGAN
# ==========================================

st.subheader("Grafik Perbandingan Proyeksi")

fig = go.Figure()

warna = {
    "SSP2-4.5": "#416E8B",
    "SSP5-8.5": "#19293B"
}

for skenario in ["SSP2-4.5", "SSP5-8.5"]:
    data_skenario = df_filter[
        df_filter["Skenario"] == skenario
    ].sort_values("Tahun")

    fig.add_trace(go.Scatter(
        x=data_skenario["Tahun"],
        y=data_skenario["Proyeksi_mm"],
        mode="lines+markers+text",
        name=skenario,
        text=data_skenario["Proyeksi_mm"].map(
            lambda x: f"{x:.1f} mm"
        ),
        textposition="top center",
        line=dict(
            color=warna[skenario],
            width=3
        ),
        marker=dict(size=10)
    ))

fig.update_layout(
    title=f"Perbandingan Proyeksi Muka Laut ({kuantil})",
    xaxis_title="Tahun",
    yaxis_title="Proyeksi (mm)",
    template="plotly_white",
    hovermode="x unified",
    legend_title="Skenario Iklim",
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TABEL PERBANDINGAN
# ==========================================

st.divider()
st.subheader("Tabel Perbandingan Nilai")

tabel = df_filter.pivot(
    index="Tahun",
    columns="Skenario",
    values="Proyeksi_mm"
).reset_index()

st.dataframe(
    tabel,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# SELISIH ANTAR SKENARIO
# ==========================================

st.divider()
st.subheader("Selisih Proyeksi Antar Skenario")

for tahun in [2035, 2045]:
    nilai_245 = df_filter.loc[
        (df_filter["Tahun"] == tahun) &
        (df_filter["Skenario"] == "SSP2-4.5"),
        "Proyeksi_mm"
    ]

    nilai_585 = df_filter.loc[
        (df_filter["Tahun"] == tahun) &
        (df_filter["Skenario"] == "SSP5-8.5"),
        "Proyeksi_mm"
    ]

    if not nilai_245.empty and not nilai_585.empty:
        selisih = nilai_585.iloc[0] - nilai_245.iloc[0]

        st.metric(
            label=f"Selisih Tahun {tahun}",
            value=f"{selisih:.1f} mm",
            help="SSP5-8.5 dikurangi SSP2-4.5."
        )

# ==========================================
# INTERPRETASI SEMENTARA
# ==========================================

st.divider()
st.subheader("Interpretasi Hasil")

st.info(f"""
**Interpretasi sementara**

Grafik menunjukkan perbandingan proyeksi muka laut
antara skenario SSP2-4.5 dan SSP5-8.5 pada kuantil {kuantil}.

Perbedaan nilai proyeksi menggambarkan perbedaan hasil
estimasi berdasarkan kedua skenario iklim tersebut.

Interpretasi lebih lanjut akan dilengkapi berdasarkan
kajian literatur dan pembahasan hasil penelitian.
""")

# ==========================================
# SUMBER DATA
# ==========================================

st.divider()
st.subheader("Sumber Data")

st.markdown("""
- **Sumber:** IPCC Sixth Assessment Report (AR6).
- **Skenario:** SSP2-4.5 dan SSP5-8.5.
- **Tahun:** 2035 dan 2045.
- **Kuantil:** P5, P50, dan P95.
- **Visualisasi:** Plotly dan Streamlit.
""")
