import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import urllib.parse

# Page configuration
st.set_page_config(page_title="Dashboard Analisis PT Victory", layout="wide")

@st.cache_data
def load_data():
SHEET_ID = "1i_6rgY7qA5Qovq2_RHFX369y4KvC4O7EcFagofBXgmM"

# Encode nama sheet (WAJIB karena ada spasi & tanda kurung)
sheet_pivot = urllib.parse.quote("Pivot Poin XAUUSD (2017-2025)")
sheet_nasabah = urllib.parse.quote("Data Nasabah (January-Juni 2026)")

# URL Google Sheets → CSV
url_pivot = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_pivot}"
url_nasabah = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_nasabah}"

# Load ke DataFrame
df_pivot = pd.read_csv(url_pivot)
df_nasabah = pd.read_csv(url_nasabah)
    
    # Cleaning Pivot Data
    df_pivot = df_pivot.dropna(subset=['Tanggal'])
    df_pivot['Tanggal'] = pd.to_datetime(df_pivot['Tanggal'])
    df_pivot['Total / Hari ($)'] = pd.to_numeric(df_pivot['Total / Hari ($)'], errors='coerce').fillna(0)
    df_pivot['Cumulative_Profit'] = df_pivot['Total / Hari ($)'].cumsum()
    df_pivot['Range ($)'] = pd.to_numeric(df_pivot['Range ($)'], errors='coerce').fillna(0)
    
    # Cleaning Nasabah Data
    df_nasabah = df_nasabah.dropna(subset=['Date'])
    df_nasabah['Date'] = pd.to_datetime(df_nasabah['Date'])
    df_nasabah['USD'] = pd.to_numeric(df_nasabah['USD'], errors='coerce').fillna(0)
    
    return df_pivot, df_nasabah

df_pivot, df_nasabah = load_data()

# Custom CSS for styling (matching reference)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .description-box {
        background-color: #e9f5ff;
        border-left: 5px solid #007bff;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Navigation
page = st.sidebar.radio("Navigasi", ["Cover", "Pivot Poin XAUUSD", "Data Nasabah"])

if page == "Cover":
    st.title("PT Victory Analytics")
    st.subheader('"Data-Driven Insights for Financial Excellence"')
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Overview Pertumbuhan Kumulatif")
        fig = px.line(df_pivot, x='Tanggal', y='Cumulative_Profit', 
                     title="Tren Pertumbuhan Ekuitas (2017-2025)",
                     template="plotly_white")
        fig.update_traces(line_color='#007bff')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Key Highlights")
        total_profit = df_pivot['Total / Hari ($)'].sum()
        max_drawdown = (df_pivot['Cumulative_Profit'].cummax() - df_pivot['Cumulative_Profit']).max()
        
        st.metric("Total Profit ($)", f"${total_profit:,.2f}")
        st.metric("Total Days Analyzed", f"{len(df_pivot)} Days")
        st.metric("Total Nasabah (2026)", f"{len(df_nasabah)}")
        
    st.markdown("""
    Grafik di atas merepresentasikan total pertumbuhan ekuitas dari strategi Pivot Point XAUUSD sejak 2017, 
    menunjukkan tren positif yang stabil sebagai fondasi bisnis PT Victory.
    """)

elif page == "Pivot Poin XAUUSD":
    st.title("Laporan Trading XAUUSD (2017-2025)")
    st.markdown("Analisis historis 9 tahun performa trading emas dengan metode Pivot Point.")
    
    # Filter Range Waktu
    min_date = df_pivot['Tanggal'].min().date()
    max_date = df_pivot['Tanggal'].max().date()
    
    st.sidebar.subheader("Filter Waktu")
    start_date, end_date = st.sidebar.date_input("Pilih Rentang Tanggal", 
                                                value=(min_date, max_date),
                                                min_value=min_date,
                                                max_value=max_date)
    
    mask = (df_pivot['Tanggal'].dt.date >= start_date) & (df_pivot['Tanggal'].dt.date <= end_date)
    df_filtered = df_pivot.loc[mask]
    
    # Visualisasi 1: Cumulative Profit
    st.subheader("1. Pertumbuhan Kumulatif Profit")
    fig1 = px.area(df_filtered, x='Tanggal', y='Cumulative_Profit', 
                   title="Akumulasi Profit terhadap Waktu",
                   template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown(f"""
    <div class="description-box">
    <b>Judul Grafik:</b> Pertumbuhan Kumulatif Keuntungan XAUUSD<br>
    <b>Menunjukkan:</b> Grafik antara Tanggal dan Akumulasi Profit ($)<br>
    <b>Interpretasi:</b> Tren menunjukkan kenaikan stabil sejak 2017 dengan fluktuasi harian yang terjaga.<br>
    <b>Manfaat:</b> Sebagai indikator utama performa jangka panjang strategi Pivot Point untuk pengambilan keputusan investasi.
    </div>
    """, unsafe_allow_html=True)
    
    # Visualisasi 2: Volatilitas (Range)
    st.subheader("2. Volatilitas Harga Harian")
    fig2 = px.bar(df_filtered, x='Tanggal', y='Range ($)', 
                  title="Rentang Harga Harian (High - Low)",
                  template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown(f"""
    <div class="description-box">
    <b>Judul Grafik:</b> Volatilitas Harian XAUUSD<br>
    <b>Menunjukkan:</b> Grafik antara Tanggal dan Range Harga ($)<br>
    <b>Interpretasi:</b> Pergerakan harga harian bervariasi secara signifikan pada periode tertentu, menunjukkan periode volatilitas tinggi.<br>
    <b>Manfaat:</b> Membantu trader mengidentifikasi risiko pasar dan menyesuaikan ukuran posisi berdasarkan volatilitas saat ini.
    </div>
    """, unsafe_allow_html=True)
    
    # Visualisasi 3: Seasonality
    st.subheader("3. Analisis Seasonality Bulanan")
    df_filtered['Month'] = df_filtered['Tanggal'].dt.month_name()
    monthly_profit = df_filtered.groupby('Month')['Total / Hari ($)'].mean().reindex([
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    
    fig3 = px.line(x=monthly_profit.index, y=monthly_profit.values, 
                  labels={'x': 'Bulan', 'y': 'Rata-rata Profit ($)'},
                  title="Rata-rata Profit Berdasarkan Bulan",
                  markers=True, template="plotly_white")
    st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown(f"""
    <div class="description-box">
    <b>Judul Grafik:</b> Seasonality Profit Bulanan<br>
    <b>Menunjukkan:</b> Grafik antara Bulan dan Rata-rata Profit per Hari<br>
    <b>Interpretasi:</b> Menemukan pola performa di mana bulan-bulan tertentu secara historis menghasilkan profit lebih konsisten.<br>
    <b>Manfaat:</b> Optimasi strategi trading dan alokasi modal berdasarkan siklus musiman harga emas.
    </div>
    """, unsafe_allow_html=True)

elif page == "Data Nasabah":
    st.title("Statistik Nasabah (January-Juni 2026)")
    st.markdown("Tinjauan demografi dan aktivitas transaksi nasabah pada semester pertama 2026.")
    
    # Filter Range Waktu
    min_date_n = df_nasabah['Date'].min().date()
    max_date_n = df_nasabah['Date'].max().date()
    
    st.sidebar.subheader("Filter Waktu")
    start_date_n, end_date_n = st.sidebar.date_input("Pilih Rentang Tanggal", 
                                                    value=(min_date_n, max_date_n),
                                                    min_value=min_date_n,
                                                    max_value=max_date_n)
    
    mask_n = (df_nasabah['Date'].dt.date >= start_date_n) & (df_nasabah['Date'].dt.date <= end_date_n)
    df_n_filtered = df_nasabah.loc[mask_n]
    
    # Visualisasi 1: Transaction Amount Over Time
    st.subheader("1. Aliran Dana Masuk (USD)")
    fig_n1 = px.line(df_n_filtered, x='Date', y='USD', 
                    title="Total Transaksi USD Harian",
                    template="plotly_white")
    st.plotly_chart(fig_n1, use_container_width=True)
    
    st.markdown(f"""
    <div class="description-box">
    <b>Judul Grafik:</b> Aliran Dana Nasabah<br>
    <b>Menunjukkan:</b> Grafik antara Tanggal dan Total Deposit/Transaksi (USD)<br>
    <b>Interpretasi:</b> Menampilkan puncak aktivitas transaksi nasabah yang berkorelasi dengan momen pasar tertentu.<br>
    <b>Manfaat:</b> Memantau likuiditas perusahaan dan efektivitas kampanye akuisisi nasabah.
    </div>
    """, unsafe_allow_html=True)
    
    # Visualisasi 2: City/Server Distribution
    st.subheader("2. Distribusi Nasabah Berdasarkan Server")
    city_counts = df_n_filtered['City'].value_counts().reset_index()
    city_counts.columns = ['Server', 'Count']
    fig_n2 = px.pie(city_counts, values='Count', names='Server', 
                    title="Proporsi Nasabah per Grup Server",
                    hole=0.4)
    st.plotly_chart(fig_n2, use_container_width=True)
    
    st.markdown(f"""
    <div class="description-box">
    <b>Judul Grafik:</b> Distribusi Nasabah per Server<br>
    <b>Menunjukkan:</b> Grafik antara Tipe Server dan Jumlah Nasabah Aktif<br>
    <b>Interpretasi:</b> Identifikasi server mana yang paling banyak digunakan oleh nasabah (MINI/MICRO/ONLINE).<br>
    <b>Manfaat:</b> Perencanaan kapasitas infrastruktur server dan penyesuaian layanan teknis berdasarkan profil nasabah.
    </div>
    """, unsafe_allow_html=True)
    
    # Visualisasi 3: Product Mix
    st.subheader("3. Komposisi Produk yang Diminati")
    prod_counts = df_n_filtered['Product'].value_counts().reset_index()
    prod_counts.columns = ['Product', 'Count']
    fig_n3 = px.bar(prod_counts, x='Product', y='Count', 
                    title="Volume Transaksi per Jenis Produk",
                    color='Product', template="plotly_white")
    st.plotly_chart(fig_n3, use_container_width=True)
    
    st.markdown(f"""
    <div class="description-box">
    <b>Judul Grafik:</b> Komposisi Produk<br>
    <b>Menunjukkan:</b> Grafik antara Jenis Produk dan Frekuensi Transaksi<br>
    <b>Interpretasi:</b> Menegaskan dominasi produk tertentu (seperti Commodity/Emas) dibanding Forex atau Indeks.<br>
    <b>Manfaat:</b> Fokus pengembangan fitur produk dan materi edukasi pada instrumen yang paling diminati pasar.
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("© 2026 PT Victory Financial. Semua Hak Dilindungi.")
