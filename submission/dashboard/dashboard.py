import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import folium
import streamlit.components.v1 as components

# Set Page Config
st.set_page_config(
    page_title="E-Commerce Public Data Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling and Theme Configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# Koordinat pusat negara bagian di Brasil (latitude & longitude)
STATE_COORDINATES = {
    'AC': (-9.7026, -68.4519), 'AL': (-9.6128, -36.0629), 'AM': (-3.3493, -60.5374),
    'AP': (0.0860, -51.2343),  'BA': (-13.0531, -39.5629), 'CE': (-4.3632, -39.0041),
    'DF': (-15.8109, -47.9696), 'ES': (-20.1106, -40.4961), 'GO': (-16.5776, -49.3342),
    'MA': (-3.7990, -44.8186), 'MG': (-19.8654, -44.4208), 'MS': (-20.7650, -54.5321),
    'MT': (-14.1609, -55.7128), 'PA': (-2.6597, -49.5130), 'PB': (-7.0971, -35.8266),
    'PE': (-8.1820, -35.7611), 'PI': (-5.7550, -42.5095), 'PR': (-24.7970, -50.8818),
    'RJ': (-22.7455, -43.1568), 'RN': (-5.8567, -35.9901), 'RO': (-10.3413, -62.7206),
    'RR': (2.7171, -60.6729),  'RS': (-29.6796, -52.0349), 'SC': (-27.2225, -49.6179),
    'SE': (-10.8662, -37.1812), 'SP': (-23.1554, -47.0842), 'TO': (-9.5037, -48.3487)
}

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
    if "is_late" not in df.columns:
        df["is_late"] = (df["delivery_status"] == "Late").astype(int)
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
    "🗺️ Sebaran Geospasial (Peta Folium)"
])

# ----------------- TAB 1: Performa Produk -----------------
with tab1:
    st.subheader("Analisis Performa Penjualan & Pendapatan Kategori Produk")
    
    cat_summary = filtered_df.groupby("product_category_name_english").agg(
        total_items=("order_item_id", "count"),
        total_revenue=("price", "sum"),
        total_orders=("order_id", "nunique"),
        avg_price=("price", "mean")
    ).reset_index()
    
    top_5_items = cat_summary.sort_values(by="total_items", ascending=False).head(5)
    top_5_rev = cat_summary.sort_values(by="total_revenue", ascending=False).head(5)
    bottom_5_items = cat_summary.sort_values(by="total_items", ascending=True).head(5)
    bottom_5_rev = cat_summary.sort_values(by="total_revenue", ascending=True).head(5)
    
    tab1_sub1, tab1_sub2 = st.tabs(["Kategori Teratas (Top Performers)", "Kategori Terendah (Lowest Performers)"])
    
    with tab1_sub1:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("**Top 5 Kategori Berdasarkan Volume Item Terjual**")
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
                ax1.annotate(f"{int(w):,} item", (w * 0.65, p.get_y() + 0.5), color="white", weight="bold")
            st.pyplot(fig1)
            
        with col_t2:
            st.markdown("**Top 5 Kategori Berdasarkan Total Pendapatan (Revenue)**")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.barplot(
                x="total_revenue", 
                y="product_category_name_english", 
                data=top_5_rev, 
                palette=["#2ca02c" if i == 0 else "#98df8a" for i in range(len(top_5_rev))],
                ax=ax2
            )
            ax2.set_xlabel("Total Pendapatan (BRL)")
            ax2.set_ylabel("")
            for p in ax2.patches:
                w = p.get_width()
                ax2.annotate(f"R$ {w/1e3:,.1f}K", (w * 0.6, p.get_y() + 0.5), color="white", weight="bold")
            st.pyplot(fig2)

    with tab1_sub2:
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown("**5 Kategori Terendah Berdasarkan Volume Item Terjual**")
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            sns.barplot(
                x="total_items", 
                y="product_category_name_english", 
                data=bottom_5_items, 
                palette=["#d62728" if i == 0 else "#ff9896" for i in range(len(bottom_5_items))],
                ax=ax3
            )
            ax3.set_xlabel("Jumlah Item Terjual")
            ax3.set_ylabel("")
            for p in ax3.patches:
                w = p.get_width()
                ax3.annotate(f"{int(w):,} item", (w + 0.1, p.get_y() + 0.5), color="black", weight="bold")
            st.pyplot(fig3)
            
        with col_b2:
            st.markdown("**5 Kategori Terendah Berdasarkan Total Pendapatan (Revenue)**")
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            sns.barplot(
                x="total_revenue", 
                y="product_category_name_english", 
                data=bottom_5_rev, 
                palette=["#ff7f0e" if i == 0 else "#ffbb78" for i in range(len(bottom_5_rev))],
                ax=ax4
            )
            ax4.set_xlabel("Total Pendapatan (BRL)")
            ax4.set_ylabel("")
            for p in ax4.patches:
                w = p.get_width()
                ax4.annotate(f"R$ {w:,.2f}", (w + 5, p.get_y() + 0.5), color="black", weight="bold")
            st.pyplot(fig4)

    st.info(
        "Temuan Kunci: Kategori dengan volume terendah belum tentu memiliki pendapatan terendah. "
        "Contohnya, 'la_cuisine' berada di 3 terendah volume item (14 item), namun mencetak revenue R$ 2.054,99 berkat harga satuan tinggi. "
        "Sebaliknya, 'home_comfort_2' laku 30 item namun revenue-nya hanya R$ 760,27."
    )

# ----------------- TAB 2: Kepuasan & Logistik -----------------
with tab2:
    st.subheader("Pengaruh Status Ketepatan Waktu Pengiriman terhadap Skor Ulasan")
    
    order_unique = filtered_df.drop_duplicates(subset=["order_id"]).copy()
    total_ord_n = len(order_unique)
    
    deliv_summary = order_unique.groupby("delivery_status").agg(
        total_orders=("order_id", "count"),
        avg_score=("review_score", "mean"),
        std_score=("review_score", "std")
    ).reset_index()
    deliv_summary["pct"] = (deliv_summary["total_orders"] / total_ord_n) * 100
    
    score_ontime = deliv_summary.loc[deliv_summary["delivery_status"] == "On Time", "avg_score"].values[0] if "On Time" in deliv_summary["delivery_status"].values else 0
    score_late = deliv_summary.loc[deliv_summary["delivery_status"] == "Late", "avg_score"].values[0] if "Late" in deliv_summary["delivery_status"].values else 0
    score_diff = score_ontime - score_late
    pct_drop = (score_diff / score_ontime) * 100 if score_ontime > 0 else 0
    
    # Pearson correlation
    r_val, p_val = stats.pearsonr(order_unique["is_late"], order_unique["review_score"])
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    col_stat1.metric("Pesanan Tepat Waktu", f"{deliv_summary.loc[deliv_summary['delivery_status'] == 'On Time', 'total_orders'].sum():,} ({deliv_summary.loc[deliv_summary['delivery_status'] == 'On Time', 'pct'].sum():.1f}%)")
    col_stat2.metric("Pesanan Terlambat", f"{deliv_summary.loc[deliv_summary['delivery_status'] == 'Late', 'total_orders'].sum():,} ({deliv_summary.loc[deliv_summary['delivery_status'] == 'Late', 'pct'].sum():.1f}%)")
    col_stat3.metric("Penurunan Skor Rata-rata", f"-{score_diff:.2f} poin ({pct_drop:.1f}%)")
    
    col_deliv1, col_deliv2 = st.columns(2)
    with col_deliv1:
        st.markdown("**Perbandingan Rata-rata Skor Ulasan**")
        fig5, ax5 = plt.subplots(figsize=(6, 4))
        sns.barplot(
            x="delivery_status", 
            y="avg_score", 
            data=deliv_summary, 
            palette=["#d62728" if s == "Late" else "#2ca02c" for s in deliv_summary["delivery_status"]],
            ax=ax5
        )
        ax5.set_ylim(0, 5)
        ax5.set_xlabel("Status Pengiriman")
        ax5.set_ylabel("Rata-rata Skor Ulasan (1-5)")
        for p in ax5.patches:
            h = p.get_height()
            ax5.annotate(f"{h:.2f}", (p.get_x() + 0.32, h / 2), color="white", weight="bold", fontsize=12)
        st.pyplot(fig5)
        
    with col_deliv2:
        st.markdown("**Distribusi Rating Bintang 1 s.d. 5 (%)**")
        cross_tab = pd.crosstab(
            order_unique["delivery_status"], 
            order_unique["review_score"].round().astype(int), 
            normalize="index"
        ) * 100
        st.dataframe(cross_tab.style.format("{:.2f}%").highlight_max(axis=1, color="#ffebee"))
        
        st.caption(
            f"Korelasi Pearson antara keterlambatan dengan review score: r = {r_val:.4f} (p-value < 0.001). "
            f"Dasar perhitungan penurunan skor: ({score_ontime:.2f} - {score_late:.2f}) / {score_ontime:.2f} * 100% = {pct_drop:.2f}%."
        )

    st.warning(
        "Catatan Metodologis: Korelasi negatif yang kuat membuktikan pesanan terlambat cenderung mendapatkan rating buruk, "
        "namun bukan klaim kausalitas tunggal karena faktor kualitas produk atau kemasan juga memengaruhi kepuasan."
    )

# ----------------- TAB 3: Segmentasi Pelanggan RFM -----------------
with tab3:
    st.subheader("Analisis RFM (Recency, Frequency, Monetary)")
    st.markdown("Segmentasi perilaku pelanggan tanpa machine learning menggunakan pengelompokan aturan bisnis (manual grouping).")
    
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
        st.markdown("**Statistik Ringkasan Pelanggan**")
        r_col, f_col, m_col = st.columns(3)
        r_col.metric("Avg Recency", f"{rfm_table['recency'].mean():.0f} hari")
        f_col.metric("Avg Frequency", f"{rfm_table['frequency'].mean():.2f} order")
        m_col.metric("Avg Monetary", f"R$ {rfm_table['monetary'].mean():.2f}")
        
        st.dataframe(rfm_table[["recency", "frequency", "monetary"]].describe().round(2))
        
    with col_rfm2:
        st.markdown("**Distribusi Segmen Pelanggan**")
        seg_counts = rfm_table["segment"].value_counts().reset_index()
        seg_counts.columns = ["Segmen", "Jumlah"]
        
        fig6, ax6 = plt.subplots(figsize=(7, 4.5))
        sns.barplot(
            x="Jumlah", 
            y="Segmen", 
            data=seg_counts, 
            palette="Blues_r",
            ax=ax6
        )
        ax6.set_xlabel("Jumlah Pelanggan")
        ax6.set_ylabel("")
        for p in ax6.patches:
            w = p.get_width()
            ax6.annotate(f"{int(w):,}", (w * 0.7, p.get_y() + 0.5), color="white", weight="bold")
        st.pyplot(fig6)

    st.success(
        "Rekomendasi CRM: Segmen 'At Risk' dan 'Potential Regulars' mencakup mayoritas basis pelanggan. "
        "Prioritaskan kampanye email dengan kupon diskon ongkir terbatas untuk mendorong transaksi kedua."
    )

# ----------------- TAB 4: Geospasial dengan Peta Folium -----------------
with tab4:
    st.subheader("Analisis Spasial Sebaran Pelanggan (Peta Interaktif Folium)")
    
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
    
    # Generate interactive Folium map
    m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4, tiles="OpenStreetMap")
    
    # Add circle markers for states with data
    max_orders_state = state_df["total_orders"].max() if not state_df.empty else 1
    for _, row in state_df.iterrows():
        uf = row["customer_state"]
        if uf in STATE_COORDINATES:
            lat, lng = STATE_COORDINATES[uf]
            rad = max(min((row["total_orders"] / max_orders_state) * 25, 25), 6)
            popup_html = (
                f"<b>Negara Bagian: {uf}</b><br>"
                f"Total Pesanan: {row['total_orders']:,}<br>"
                f"Total Pelanggan: {row['total_customers']:,}<br>"
                f"Total Revenue: R$ {row['total_revenue']:,.2f}<br>"
                f"Rata-rata Ongkir: R$ {row['avg_freight']:,.2f}"
            )
            folium.CircleMarker(
                location=[lat, lng],
                radius=rad,
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{uf}: {row['total_orders']:,} pesanan",
                color="#1f77b4",
                fill=True,
                fill_color="#1f77b4",
                fill_opacity=0.6
            ).add_to(m)
            
    col_map, col_table = st.columns([1.2, 1])
    with col_map:
        st.markdown("**Peta Sebaran Pelanggan per Wilayah di Brasil**")
        components.html(m._repr_html_(), height=480)
        
    with col_table:
        st.markdown("**Rincian Kinerja Wilayah (Top 10 States)**")
        st.dataframe(
            state_df.head(10).style.format({
                "total_orders": "{:,}",
                "total_customers": "{:,}",
                "total_revenue": "R$ {:,.2f}",
                "avg_freight": "R$ {:,.2f}"
            })
        )

    st.info(
        "Insight Geospasial: Konsentrasi terbesar berada di wilayah Tenggara (São Paulo, Rio de Janeiro, Minas Gerais). "
        "Wilayah ini mendominasi lebih dari 65% total pesanan nasional dengan ongkos kirim paling ekonomis."
    )
