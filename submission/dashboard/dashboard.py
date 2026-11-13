import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set Page Config
st.set_page_config(
    page_title="E-Commerce Public Data Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling and Theme Configuration (Anti-Slop Clean Aesthetic)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# Helper to load data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    possible_paths = [
        os.path.join(base_dir, "main_data.csv"),
        os.path.join(base_dir, "..", "dashboard", "main_data.csv"),
        os.path.join(os.getcwd(), "submission", "dashboard", "main_data.csv"),
        "submission/dashboard/main_data.csv",
        "dashboard/main_data.csv",
        "main_data.csv"
    ]
    data_path = None
    for p in possible_paths:
        if os.path.exists(p):
            data_path = p
            break
            
    if data_path is None:
        st.error("File data tidak ditemukan. Pastikan main_data.csv tersedia.")
        return None
        
    df = pd.read_csv(data_path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_purchase_date"] = pd.to_datetime(df["order_purchase_date"]).dt.date
    return df

df_raw = load_data()

if df_raw is None or df_raw.empty:
    st.warning("Data kosong atau belum dimuat dengan benar.")
    st.stop()

# Sidebar: Filter Interaktif
st.sidebar.header("Filter Analisis")
min_date = df_raw["order_purchase_date"].min()
max_date = df_raw["order_purchase_date"].max()

date_range = st.sidebar.date_input(
    "Rentang Tanggal Pembelian:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Handle single date or range selection
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
    start_date = end_date = date_range[0]
else:
    start_date, end_date = min_date, max_date

# Filter State
state_list = ["Semua"] + sorted(df_raw["customer_state"].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("Pilih Negara Bagian (State):", state_list)

# Apply filters
filtered_df = df_raw[
    (df_raw["order_purchase_date"] >= start_date) &
    (df_raw["order_purchase_date"] <= end_date)
]
if selected_state != "Semua":
    filtered_df = filtered_df[filtered_df["customer_state"] == selected_state]

# Empty State Check
if filtered_df.empty:
    st.warning("Tidak ada transaksi yang cocok dengan filter yang dipilih.")
    st.stop()

# Header Dashboard
st.title("🛒 Brazilian E-Commerce Analytics Dashboard")
st.caption(f"Data Transaksi Periode: {start_date.strftime('%d %B %Y')} s.d. {end_date.strftime('%d %B %Y')}")

# KPI Cards
total_orders = filtered_df["order_id"].nunique()
total_revenue = filtered_df["payment_value"].sum()
total_customers = filtered_df["customer_unique_id"].nunique()
avg_review = filtered_df["review_score"].mean()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Pesanan", f"{total_orders:,}")
with col2:
    st.metric("Total Pendapatan", f"R$ {total_revenue:,.2f}")
with col3:
    st.metric("Total Pelanggan", f"{total_customers:,}")
with col4:
    st.metric("Rata-rata Rating", f"{avg_review:.2f} / 5.00")

st.markdown("---")

# Tab Navigasi Utama
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Performa Produk", 
    "🚚 Kepuasan & Pengiriman", 
    "👥 Segmentasi Pelanggan (RFM)", 
    "🗺️ Sebaran Geospasial"
])

# ----------------- TAB 1: Performa Produk -----------------
with tab1:
    st.subheader("Analisis Performa Penjualan Berdasarkan Kategori Produk")
    
    cat_summary = filtered_df.groupby("product_category_name_english").agg(
        total_items=("order_item_id", "count"),
        total_revenue=("price", "sum"),
        avg_price=("price", "mean")
    ).reset_index()
    
    top_5_items = cat_summary.sort_values(by="total_items", ascending=False).head(5)
    bottom_5_items = cat_summary.sort_values(by="total_items", ascending=True).head(5)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**Top 5 Kategori Terlaris (Volume Item)**")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.barplot(
            x="total_items", 
            y="product_category_name_english", 
            data=top_5_items, 
            palette=["#1f77b4" if i == 0 else "#aec7e8" for i in range(len(top_5_items))],
            ax=ax1
        )
        ax1.set_xlabel("Jumlah Item Terjual")
        ax1.set_ylabel("")
        for p in ax1.patches:
            w = p.get_width()
            ax1.annotate(f"{int(w):,}", (w * 0.75, p.get_y() + 0.5), color="white", weight="bold")
        st.pyplot(fig1)
        
    with col_chart2:
        st.markdown("**5 Kategori dengan Volume Terendah**")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.barplot(
            x="total_items", 
            y="product_category_name_english", 
            data=bottom_5_items, 
            palette=["#d62728" if i == 0 else "#ff9896" for i in range(len(bottom_5_items))],
            ax=ax2
        )
        ax2.set_xlabel("Jumlah Item Terjual")
        ax2.set_ylabel("")
        for p in ax2.patches:
            w = p.get_width()
            ax2.annotate(f"{int(w):,}", (w + 0.2, p.get_y() + 0.5), color="black", weight="bold")
        st.pyplot(fig2)

    st.info(
        "Insight Bisnis: Kategori perabot rumah tangga (bed_bath_table) dan kesehatan/kecantikan (health_beauty) "
        "merupakan penopang volume penjualan utama. Kategori dengan penjualan terendah membutuhkan evaluasi stok dan kurasi katalog."
    )

# ----------------- TAB 2: Kepuasan & Logistik -----------------
with tab2:
    st.subheader("Dampak Ketepatan Waktu Pengiriman terhadap Skor Ulasan Pelanggan")
    
    delivery_perf = filtered_df.groupby("delivery_status").agg(
        avg_score=("review_score", "mean"),
        total_orders=("order_id", "nunique")
    ).reset_index()
    
    col_deliv1, col_deliv2 = st.columns(2)
    
    with col_deliv1:
        st.markdown("**Rata-rata Skor Ulasan: Tepat Waktu vs Terlambat**")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        colors = ["#d62728" if s == "Late" else "#2ca02c" for s in delivery_perf["delivery_status"]]
        sns.barplot(
            x="delivery_status", 
            y="avg_score", 
            data=delivery_perf, 
            palette=colors,
            ax=ax3
        )
        ax3.set_ylim(0, 5)
        ax3.set_xlabel("Status Pengiriman")
        ax3.set_ylabel("Rata-rata Skor Ulasan (1-5)")
        for p in ax3.patches:
            h = p.get_height()
            ax3.annotate(f"{h:.2f}", (p.get_x() + 0.32, h / 2), color="white", weight="bold", fontsize=12)
        st.pyplot(fig3)
        
    with col_deliv2:
        st.markdown("**Distribusi Rating Bintang (1 s.d. 5) Berdasarkan Status**")
        cross_tab = pd.crosstab(
            filtered_df["delivery_status"], 
            filtered_df["review_score"].round().astype(int), 
            normalize="index"
        ) * 100
        
        st.dataframe(cross_tab.style.format("{:.2f}%").highlight_max(axis=1, color="#ffebee"))
        
        st.caption(
            "Pesanan yang terlambat memiliki lonjakan rating bintang 1 hingga lebih dari 45%, "
            "sedangkan pesanan tepat waktu didominasi oleh rating bintang 5 (>60%)."
        )

    st.error(
        "Rekomendasi Operasional: Keterlambatan pengiriman adalah pemicu utama ulasan negatif. "
        "Diperlukan evaluasi SLA mitra ekspedisi dan penambahan estimasi waktu yang lebih realistis."
    )

# ----------------- TAB 3: Segmentasi Pelanggan RFM -----------------
with tab3:
    st.subheader("Analisis RFM (Recency, Frequency, Monetary)")
    st.markdown("Segmentasi perilaku pelanggan tanpa machine learning menggunakan manual grouping.")
    
    ref_date = filtered_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
    
    rfm_table = filtered_df.groupby("customer_unique_id").agg({
        "order_purchase_timestamp": lambda x: (ref_date - x.max()).days,
        "order_id": "nunique",
        "price": "sum"
    }).reset_index()
    
    rfm_table.columns = ["customer_unique_id", "recency", "frequency", "monetary"]
    
    def get_rfm_segment(row):
        if row["frequency"] >= 2 and row["recency"] <= 120:
            return "Champions"
        elif row["frequency"] >= 2 and row["recency"] > 120:
            return "Loyal Customers"
        elif row["frequency"] == 1 and row["recency"] <= 90:
            return "New Customers"
        elif row["frequency"] == 1 and 90 < row["recency"] <= 270:
            return "Potential Regulars"
        elif row["frequency"] == 1 and 270 < row["recency"] <= 450:
            return "At Risk"
        else:
            return "Lost Customers"
            
    rfm_table["segment"] = rfm_table.apply(get_rfm_segment, axis=1)
    
    col_rfm1, col_rfm2 = st.columns([1, 1])
    
    with col_rfm1:
        st.markdown("**Metrik Rata-rata Pelanggan**")
        r_col, f_col, m_col = st.columns(3)
        r_col.metric("Avg Recency", f"{rfm_table['recency'].mean():.0f} hari")
        f_col.metric("Avg Frequency", f"{rfm_table['frequency'].mean():.2f} order")
        m_col.metric("Avg Monetary", f"R$ {rfm_table['monetary'].mean():.2f}")
        
        st.dataframe(
            rfm_table[["recency", "frequency", "monetary"]].describe().round(2)
        )
        
    with col_rfm2:
        st.markdown("**Distribusi Segmen Pelanggan**")
        seg_counts = rfm_table["segment"].value_counts().reset_index()
        seg_counts.columns = ["Segmen", "Jumlah"]
        
        fig4, ax4 = plt.subplots(figsize=(7, 4.5))
        sns.barplot(
            x="Jumlah", 
            y="Segmen", 
            data=seg_counts, 
            palette="Blues_r",
            ax=ax4
        )
        ax4.set_xlabel("Jumlah Pelanggan")
        ax4.set_ylabel("")
        for p in ax4.patches:
            w = p.get_width()
            ax4.annotate(f"{int(w):,}", (w * 0.7, p.get_y() + 0.5), color="white", weight="bold")
        st.pyplot(fig4)

    st.success(
        "Strategi Marketing: Segmen At Risk dan Potential Regulars mencakup basis pelanggan terbesar. "
        "Program re-aktivasi berkala melalui voucher ongkir sangat disarankan untuk mendorong pesanan kedua."
    )

# ----------------- TAB 4: Geospasial -----------------
with tab4:
    st.subheader("Sebaran Aktivitas Transaksi Berdasarkan Negara Bagian (State)")
    
    state_df = filtered_df.groupby("customer_state").agg({
        "order_id": "nunique",
        "customer_unique_id": "nunique",
        "price": "sum",
        "freight_value": "mean"
    }).reset_index().rename(columns={
        "order_id": "total_orders",
        "customer_unique_id": "total_customers",
        "price": "total_revenue",
        "freight_value": "avg_freight"
    }).sort_values(by="total_orders", ascending=False)
    
    col_geo1, col_geo2 = st.columns(2)
    
    with col_geo1:
        st.markdown("**Top 10 Negara Bagian Berdasarkan Jumlah Pesanan**")
        top_10 = state_df.head(10)
        fig5, ax5 = plt.subplots(figsize=(6, 4.5))
        sns.barplot(
            x="total_orders", 
            y="customer_state", 
            data=top_10, 
            palette="crest",
            ax=ax5
        )
        ax5.set_xlabel("Total Pesanan")
        ax5.set_ylabel("State")
        for p in ax5.patches:
            w = p.get_width()
            ax5.annotate(f"{int(w):,}", (w * 0.65, p.get_y() + 0.5), color="white", weight="bold")
        st.pyplot(fig5)
        
    with col_geo2:
        st.markdown("**Tabel Rincian Kinerja Wilayah**")
        st.dataframe(
            state_df.head(10).style.format({
                "total_orders": "{:,}",
                "total_customers": "{:,}",
                "total_revenue": "R$ {:,.2f}",
                "avg_freight": "R$ {:,.2f}"
            })
        )

    st.info(
        "Insight Wilayah: Negara bagian São Paulo (SP), Rio de Janeiro (RJ), dan Minas Gerais (MG) "
        "adalah pusat transaksi terbesar. Penempatan gudang fulfillment di area ini akan memangkas durasi kirim secara drastis."
    )
