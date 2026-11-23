
import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

# Lokasi folder data
DATA_DIR = "data"

# Membaca dataset
df_historis = pd.read_csv(
    os.path.join(DATA_DIR, "Data_Historis_SLA_Dashboard_AR1.csv")
)

df_proyeksi = pd.read_csv(
    os.path.join(DATA_DIR, "Proyeksi_AR6_2035_2045.csv")
)

# Konfigurasi halaman
st.set_page_config(
    page_title="Sea Level Rise - Teluk Jakarta",
    page_icon="🌊",
    layout="wide"
)

# ==========================================
# HEADER UTAMA DASHBOARD
# ==========================================

st.markdown("""
<style>
.header-dashboard {
    position: relative;
    width: 100%;
    background-color: #183B56;
    padding: 15px 25px;
    box-sizing: border-box;
    margin: 0;
    display: block;
}

.header-dashboard h1 {
    color: white;
    font-size: 30px;
    font-weight: 700;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
}

.header-dashboard p {
    color: #D6E5F0;
    font-size: 13px;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
}

div[data-testid="stMainBlockContainer"] {
    padding-top: 15px !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 20px !important;
}

</style>

<div class="header-dashboard">
    <h1>SEA LEVEL RISE DASHBOARD</h1>
    <p>Analisis Historis dan Proyeksi Kenaikan Muka Laut di Teluk Jakarta</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# NAVIGASI SIDEBAR
# ==========================================

st.sidebar.title("🌊Sea Level Rise")
st.sidebar.caption("Teluk Jakarta")

# ==========================================
# NAVIGASI SIDEBAR BERBENTUK KOTAK
# ==========================================

if "menu" not in st.session_state:
    st.session_state.menu = "Beranda"

daftar_menu = [
    ("Beranda", ":material/home:"),
    ("Analisis Historis SLA", ":material/monitoring:"),
    ("Proyeksi IPCC AR6", ":material/trending_up:"),
    ("Perbandingan Skenario", ":material/analytics:"),
    ("Data Proyeksi", ":material/table_chart:"),
    ("Metodologi Penelitian", ":material/menu_book:"),
    ("Jurnal dan Referensi", ":material/library_books:")
]

for nama, ikon in daftar_menu:
    if st.sidebar.button(
        nama,
        icon=ikon,
        key=f"menu_{nama}",
        use_container_width=True,
        type="primary" if st.session_state.menu == nama else "secondary"
    ):
        st.session_state.menu = nama

menu = st.session_state.menu

st.sidebar.divider()

st.sidebar.caption(
    "Analisis Historis dan Proyeksi "
    "Kenaikan Muka Laut"
)

st.divider()
if menu == "Beranda":  
   
    st.markdown("""
    Dashboard ini menyajikan hasil analisis perubahan Sea Level Anomaly (SLA)
    historis berdasarkan data satellite altimetry serta proyeksi kenaikan muka
    laut berdasarkan skenario IPCC AR6.
    """)

    st.divider()

    # Ringkasan penelitian
    st.header("Ringkasan Hasil Penelitian")

    col1, col2, col3 = st.columns([1.4, 1, 1])

    with col1:
        st.metric(
            label="Tren Historis SLA",
            value="4,231 mm/tahun",
            help="Estimasi tren berdasarkan model SARIMAX AR(1)"
        )

    with col2:
        st.metric(
            label="Periode Historis",
            value="1993–2025"
        )

    with col3:
        st.metric(
            label="Tahun Proyeksi",
            value="2035–2045"
        )

    st.divider()

    st.header("Tentang Dashboard")

    st.write("""
    Dashboard ini dikembangkan untuk memvisualisasikan:
    - Perubahan SLA historis di sekitar Tanjung Priok.
    - Estimasi tren historis menggunakan model AR(1).
    - Proyeksi muka laut IPCC AR6 berdasarkan skenario SSP2-4.5 dan SSP5-8.5.
    - Perbandingan kuantil P5, P50, dan P95.
    """)

    st.caption("Sumber data: Copernicus Marine Service dan IPCC AR6.")
    st.caption("Pengolahan data: Python | Visualisasi: Streamlit")

elif menu == "Analisis Historis SLA":

    # ==========================================
    # ANALISIS HISTORIS SLA
    # ==========================================

    st.divider()
    st.header("Analisis Historis Sea Level Anomaly (SLA)")

    # Mengubah tanggal menjadi datetime
    df_historis["tanggal"] = pd.to_datetime(df_historis["tanggal"])

    # Filter rentang tahun
    tahun_min = int(df_historis["tanggal"].dt.year.min())
    tahun_max = int(df_historis["tanggal"].dt.year.max())

    rentang_tahun = st.slider(
        "Pilih Rentang Tahun",
        min_value=tahun_min,
        max_value=tahun_max,
        value=(tahun_min, tahun_max),
        step=1
    )

    # Filter data
    df_filter = df_historis[
        (df_historis["tanggal"].dt.year >= rentang_tahun[0]) &
        (df_historis["tanggal"].dt.year <= rentang_tahun[1])
    ].copy()

    # Informasi jumlah data
    st.caption(
        f"Periode: {rentang_tahun[0]}–{rentang_tahun[1]} | "
        f"Jumlah observasi: {len(df_filter)} bulan"
    )

    # Grafik interaktif
    import plotly.graph_objects as go

    fig_historis = go.Figure()

    # SLA aktual
    fig_historis.add_trace(
        go.Scatter(
            x=df_filter["tanggal"],
            y=df_filter["SLA_Rata_Rata"] * 1000,
            mode="lines",
            name="SLA Aktual",
            line=dict(width=1.5),
            hovertemplate="%{x|%b %Y}<br>SLA: %{y:.2f} mm<extra></extra>"
        )
    )

    # Fitted SARIMAX
    fig_historis.add_trace(
        go.Scatter(
            x=df_filter["tanggal"],
            y=df_filter["Fitted_SARIMAX"] * 1000,
            mode="lines",
            name="Fitted SARIMAX (AR1)",
            line=dict(width=2),
            hovertemplate="%{x|%b %Y}<br>Fitted: %{y:.2f} mm<extra></extra>"
        )
    )

    fig_historis.update_layout(
        title=f"Perubahan Historis Sea Level Anomaly ({rentang_tahun[0]}–{rentang_tahun[1]})",
        xaxis_title="Tahun",
        yaxis_title="Sea Level Anomaly (mm)",
        hovermode="x unified",
        legend_title="Keterangan",
        template="plotly_white",
        height=550
    )

    fig_historis.update_xaxes(
        showgrid=True,
        rangeslider_visible=True
    )

    fig_historis.update_yaxes(showgrid=True)

    st.plotly_chart(fig_historis, use_container_width=True)

elif menu == "Proyeksi IPCC AR6":
    # ==========================================
    # PROYEKSI KENAIKAN MUKA LAUT IPCC AR6
    # ==========================================

    st.divider()
    st.header("Proyeksi Kenaikan Muka Laut IPCC AR6")

    # Pilihan skenario
    pilihan_skenario = st.selectbox(
        "Pilih Skenario IPCC",
        ["SSP2-4.5", "SSP5-8.5"]
    )

    # Pilihan kuantil
    pilihan_kuantil = st.selectbox(
        "Pilih Kuantil",
        ["P5", "P50", "P95"],
        index=1
    )

    # Filter data proyeksi
    df_proyeksi_filter = df_proyeksi[
        (df_proyeksi["Skenario"] == pilihan_skenario) &
        (df_proyeksi["Kuantil"] == pilihan_kuantil)
    ].copy()

    # Grafik proyeksi
    fig_proyeksi = go.Figure()

    fig_proyeksi.add_trace(
        go.Scatter(
            x=df_proyeksi_filter["Tahun"],
            y=df_proyeksi_filter["Proyeksi_mm"],
            mode="lines+markers",
            name=f"{pilihan_skenario} - {pilihan_kuantil}",
            line=dict(width=3),
            marker=dict(size=10)
        )
    )

    fig_proyeksi.update_layout(
        title=f"Proyeksi Kenaikan Muka Laut ({pilihan_skenario} - {pilihan_kuantil})",
        xaxis_title="Tahun",
        yaxis_title="Perubahan Muka Laut (mm)",
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(fig_proyeksi, use_container_width=True)

elif menu == "Perbandingan Skenario":
    # ==========================================
    # PERBANDINGAN SKENARIO IPCC AR6
    # ==========================================

    st.divider()
    st.header("Perbandingan Skenario IPCC AR6")
    pilihan_kuantil = st.selectbox(
    "Pilih Kuantil",
    ["P5", "P50", "P95"],
    key="kuantil_perbandingan"
    )
    st.write(
        "Perbandingan proyeksi kenaikan muka laut "
        "antara skenario SSP2-4.5 dan SSP5-8.5."
    )

    # Filter berdasarkan kuantil yang dipilih
    df_perbandingan = df_proyeksi[
        df_proyeksi["Kuantil"] == pilihan_kuantil
    ].copy()

    fig_perbandingan = go.Figure()

    # Garis SSP2-4.5
    for skenario in ["SSP2-4.5", "SSP5-8.5"]:
        df_skenario = df_perbandingan[
            df_perbandingan["Skenario"] == skenario
        ].sort_values("Tahun")

        fig_perbandingan.add_trace(
            go.Scatter(
                x=df_skenario["Tahun"],
                y=df_skenario["Proyeksi_mm"],
                mode="lines+markers",
                name=skenario,
                line=dict(width=3),
                marker=dict(size=10)
            )
        )

    fig_perbandingan.update_layout(
        title=f"Perbandingan Proyeksi Muka Laut ({pilihan_kuantil})",
        xaxis_title="Tahun",
        yaxis_title="Perubahan Muka Laut (mm)",
        hovermode="x unified",
        template="plotly_white",
        legend_title="Skenario IPCC"
    )

    st.plotly_chart(
        fig_perbandingan,
        use_container_width=True
    )

elif menu == "Data Proyeksi":
    # ==========================================
    # TABEL DATA PROYEKSI AR6
    # ==========================================

    st.divider()
    st.header("Tabel Data Proyeksi IPCC AR6")

    # Filter tabel
    col1, col2 = st.columns(2)

    with col1:
        filter_skenario = st.selectbox(
            "Filter Skenario",
            ["Semua Skenario", "SSP2-4.5", "SSP5-8.5"],
            key="tabel_skenario"
        )

    with col2:
        filter_kuantil = st.selectbox(
            "Filter Kuantil",
            ["Semua Kuantil", "P5", "P50", "P95"],
            key="tabel_kuantil"
        )

    df_tabel = df_proyeksi.copy()

    if filter_skenario != "Semua Skenario":
        df_tabel = df_tabel[
            df_tabel["Skenario"] == filter_skenario
        ]

    if filter_kuantil != "Semua Kuantil":
        df_tabel = df_tabel[
            df_tabel["Kuantil"] == filter_kuantil
        ]

    df_tabel = df_tabel.sort_values(
        ["Skenario", "Kuantil", "Tahun"]
    )

    st.dataframe(
        df_tabel,
        use_container_width=True,
        hide_index=True
    )
