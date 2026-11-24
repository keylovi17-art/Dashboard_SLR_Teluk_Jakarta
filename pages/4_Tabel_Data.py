
import streamlit as st
import pandas as pd
import os

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Tabel Data - Teluk Jakarta",
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
    font-weight: 700;
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

st.title("Tabel Data Proyeksi Muka Laut")

st.markdown("""
Halaman ini menyajikan nilai proyeksi perubahan muka laut
berdasarkan skenario iklim IPCC AR6. Gunakan filter untuk
menelusuri data berdasarkan skenario, tingkat kuantil,
dan tahun proyeksi.
""")

st.divider()

# ==========================================
# FILTER DATA
# ==========================================

st.subheader("Filter Data")

col1, col2, col3 = st.columns(3)

with col1:
    pilihan_skenario = st.multiselect(
        "Pilih skenario",
        options=sorted(df["Skenario"].unique()),
        default=sorted(df["Skenario"].unique())
    )

with col2:
    pilihan_kuantil = st.multiselect(
        "Pilih kuantil",
        options=["P5", "P50", "P95"],
        default=["P5", "P50", "P95"]
    )

with col3:
    pilihan_tahun = st.multiselect(
        "Pilih tahun",
        options=sorted(df["Tahun"].unique()),
        default=sorted(df["Tahun"].unique())
    )

df_filter = df[
    (df["Skenario"].isin(pilihan_skenario)) &
    (df["Kuantil"].isin(pilihan_kuantil)) &
    (df["Tahun"].isin(pilihan_tahun))
].copy()

# ==========================================
# RINGKASAN DATA
# ==========================================

st.divider()
st.subheader("Ringkasan Data")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Jumlah Data", len(df_filter))

with col2:
    st.metric(
        "Jumlah Skenario",
        df_filter["Skenario"].nunique()
    )

with col3:
    st.metric(
        "Jumlah Tahun",
        df_filter["Tahun"].nunique()
    )

# ==========================================
# TABEL DATA
# ==========================================

st.divider()
st.subheader("Data Proyeksi")

tabel = df_filter.sort_values(
    ["Skenario", "Kuantil", "Tahun"]
).reset_index(drop=True)

st.dataframe(
    tabel,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Skenario": st.column_config.TextColumn(
            "Skenario Iklim"
        ),
        "Kuantil": st.column_config.TextColumn(
            "Kuantil"
        ),
        "Tahun": st.column_config.NumberColumn(
            "Tahun",
            format="%d"
        ),
        "Proyeksi_mm": st.column_config.NumberColumn(
            "Proyeksi (mm)",
            format="%.1f"
        )
    }
)

# ==========================================
# UNDUH DATA
# ==========================================

st.divider()
st.subheader("Unduh Data")

csv = tabel.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Unduh Data dalam Format CSV",
    data=csv,
    file_name="Data_Proyeksi_SLR_Teluk_Jakarta.csv",
    mime="text/csv"
)

# ==========================================
# INFORMASI DATA
# ==========================================

st.divider()
st.subheader("Keterangan Data")

st.markdown("""
- **Skenario:** SSP2-4.5 dan SSP5-8.5.
- **Kuantil:** P5, P50, dan P95.
- **Tahun proyeksi:** 2035 dan 2045.
- **Satuan:** milimeter (mm).
- **Sumber:** IPCC Sixth Assessment Report (AR6).
""")

st.info("""
Data proyeksi menggunakan grid regional terdekat dengan
wilayah kajian. Nilainya tidak merepresentasikan pengukuran
langsung di garis pantai Tanjung Priok.
""")
