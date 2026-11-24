import streamlit as st
st.set_page_config(
    page_title="Sea Level Rise Dashboard - Teluk Jakarta",
    page_icon="🌊",
    layout="wide"
)

# HEADER GLOBAL DASHBOARD
st.markdown("""
<style>
.header-dashboard {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 999999;
    background-color: #253E51;
    padding: 16px 30px;
    box-sizing: border-box;
    margin: 0;
}

[data-testid="stAppViewContainer"] {
    padding-top: 90px;
}

.header-dashboard h1 {
    color: white;
    font-size: 30px;
    font-weight: 700;
    margin: 0;
    padding: 0;
}

.header-dashboard p {
    color: #D6E5F0;
    font-size: 14px;
    margin: 4px 0 0 0;
}
</style>

<div class="header-dashboard">
    <h1>SEA LEVEL RISE DASHBOARD</h1>
    <p>Analisis Historis dan Proyeksi Kenaikan Muka Laut di Teluk Jakarta</p>
</div>
""", unsafe_allow_html=True)

st.subheader(
    "Memahami perubahan muka laut, dari pengamatan historis "
    "hingga proyeksi masa depan."
)

st.markdown("""
Dashboard ini mengajak Anda melihat bagaimana muka laut di wilayah
Teluk Jakarta berubah dari waktu ke waktu dan bagaimana kondisinya
diproyeksikan pada masa mendatang.

Melalui data satelit altimetri dan proyeksi IPCC AR6, dashboard ini
menyajikan tren historis *Sea Level Anomaly* (SLA), estimasi kenaikan
muka laut untuk beberapa skenario iklim, serta perbandingan hasil
proyeksi berdasarkan tingkat kuantil.

Jelajahi setiap halaman melalui menu navigasi di sebelah kiri untuk
melihat grafik, memahami hasil analisis, dan membandingkan proyeksi
muka laut pada tahun 2035 dan 2045.
""")

st.divider()

st.header("Ringkasan Hasil Penelitian")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Tren Historis SLA",
        value="4,231 mm/tahun",
        help="Estimasi tren dari model SARIMAX AR(1)."
    )

with col2:
    st.metric(
        label="Periode Pengamatan",
        value="1993–2025",
        help="396 observasi bulanan."
    )

with col3:
    st.metric(
        label="Periode Proyeksi",
        value="2035–2045"
    )

st.caption(
    "Tren historis dihitung menggunakan model SARIMAX dengan "
    "komponen autoregresif AR(1)."
)

st.divider()

st.header("Gambaran Proyeksi IPCC AR6")

st.write(
    "Berikut nilai median (P50) proyeksi perubahan muka laut "
    "berdasarkan dua skenario iklim yang dianalisis."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("SSP2-4.5")
    st.metric("Tahun 2035", "119,5 mm")
    st.metric("Tahun 2045", "177,5 mm")

with col2:
    st.subheader("SSP5-8.5")
    st.metric("Tahun 2035", "131,5 mm")
    st.metric("Tahun 2045", "201 mm")

st.caption(
    "Nilai merupakan proyeksi P50 terhadap acuan IPCC 1995–2014."
)

st.divider()

st.header("Sumber dan Pengolahan Data")

st.markdown("""
- **Copernicus Marine Service:** data historis Sea Level Anomaly
  dari satelit altimetri, 1993–2025.
- **IPCC AR6:** data proyeksi muka laut untuk skenario SSP2-4.5
  dan SSP5-8.5.
- **Pengolahan data:** Python, Pandas, dan Statsmodels.
- **Visualisasi:** Plotly dan Streamlit.
""")

st.info(
    "Catatan: Data proyeksi IPCC menggunakan grid regional terdekat "
    "dengan wilayah kajian, sehingga tidak merepresentasikan "
    "pengukuran langsung di garis pantai Tanjung Priok."
)

