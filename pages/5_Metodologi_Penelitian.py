import streamlit as st

# HEADER GLOBAL DASHBOARD
st.markdown("""

<style>
.header-dashboard {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    height: 95px;
    background-color: #253E51;
    padding: 16px 30px;
    box-sizing: border-box;
    z-index: 999999;
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

/* Memberi ruang untuk header fixed */
[data-testid="stAppViewContainer"] {
    padding-top: 110px;
}
</style>

""", unsafe_allow_html=True)

# JUDUL HALAMAN
st.title("Metodologi Penelitian")

st.markdown("""
Halaman ini menjelaskan tahapan pengolahan data yang digunakan
untuk menganalisis perubahan Sea Level Anomaly (SLA) historis
dan proyeksi kenaikan muka laut di perairan Teluk Jakarta.
""")

st.divider()

# 1. DATA HISTORIS
st.header("1. Pengumpulan Data Historis")

st.write("""
Data historis diperoleh dari Copernicus Marine Service berupa
Sea Level Anomaly (SLA) bulanan periode Januari 1993 hingga
Desember 2025, dengan total 396 observasi.

Data menggunakan dua grid terdekat, yaitu G33 dan G34.
Kedua nilai tersebut dirata-ratakan untuk membentuk satu
seri waktu historis yang digunakan dalam analisis.
""")

# 2. DATA PROYEKSI
st.header("2. Pengumpulan Data Proyeksi IPCC AR6")

st.write("""
Data proyeksi diperoleh dari IPCC AR6 untuk dua skenario
perubahan iklim, yaitu SSP2-4.5 dan SSP5-8.5.

Analisis menggunakan kuantil P5, P50, dan P95 untuk
menggambarkan rentang proyeksi. Data berasal dari grid
regional terdekat dengan wilayah kajian.
""")

# 3. PENGOLAHAN HISTORIS
st.header("3. Pengolahan Data Historis")

st.write("""
Data SLA dari kedua grid dirata-ratakan dan disusun menjadi
deret waktu bulanan. Selanjutnya, data digunakan untuk
mengidentifikasi kecenderungan perubahan muka laut selama
periode pengamatan.
""")

# 4. ANALISIS STATISTIK
st.header("4. Analisis Tren Menggunakan SARIMAX")

st.write("""
Analisis tren dilakukan menggunakan model SARIMAX(1,0,0)
dengan variabel tren waktu dan dummy bulanan. Komponen
autoregresif AR(1) digunakan untuk mempertimbangkan
autokorelasi pada data deret waktu.
""")

col1, col2 = st.columns(2)

with col1:
    st.metric("Estimasi Tren Historis", "4,231 mm/tahun")

with col2:
    st.metric("Jumlah Observasi", "396 bulan")

# 5. PROYEKSI
st.header("5. Pengolahan Data Proyeksi")

st.write("""
Nilai proyeksi IPCC AR6 untuk tahun 2035 dan 2045 diperoleh
melalui interpolasi linear dari data dekadal. Pengolahan
dilakukan untuk masing-masing skenario SSP2-4.5 dan SSP5-8.5
serta kuantil P5, P50, dan P95.
""")

# 6. VISUALISASI
st.header("6. Visualisasi dan Penyajian Hasil")

st.write("""
Hasil pengolahan disajikan dalam bentuk grafik perubahan SLA
historis, grafik proyeksi, perbandingan skenario, serta tabel
data. Visualisasi dashboard dibuat menggunakan Plotly dan
Streamlit.
""")

st.divider()

# CATATAN METODOLOGI
st.subheader("Catatan Metodologis")

st.info("""
Data proyeksi IPCC AR6 menggunakan grid regional terdekat
yang berjarak sekitar 19,79 km dari titik acuan Tanjung Priok.
Oleh karena itu, data tersebut tidak merepresentasikan
pengukuran langsung di garis pantai.

Proyeksi ini juga belum memasukkan komponen penurunan muka
tanah lokal (land subsidence).
""")

st.caption(
    "Pengolahan data dilakukan menggunakan Python, Pandas, "
    "NumPy, dan Statsmodels."
)
