# Proyek Analisis Data: E-Commerce Public Dataset

Proyek akhir analisis data kelas **Belajar Analisis Data dengan Python** dari Dicoding Indonesia. Proyek ini mencakup seluruh tahapan analisis data mulai dari perumusan pertanyaan bisnis SMART, Data Wrangling, Exploratory Data Analysis (EDA), Visualisasi Data interaktif, Analisis Lanjutan (RFM & Geospatial), hingga pembuatan dashboard analitik interaktif berbasis Streamlit.

---

## 1. Pertanyaan Bisnis (SMART Method)
1. **Performa Kategori Produk (2017 - 2018):** Kategori produk apa saja yang mencatatkan volume penjualan (jumlah item terjual) dan pendapatan (*revenue*) tertinggi serta terendah sepanjang tahun 2017 sampai 2018?
2. **Kualitas Pengiriman & Kepuasan Pelanggan (2017 - 2018):** Bagaimana korelasi antara keterlambatan pengiriman (*delivery delay*) terhadap rata-rata skor ulasan (*customer review score*) pada transaksi tahun 2017 sampai 2018?
3. **Analisis Lanjutan:**
   - **RFM Analysis:** Segmentasi pelanggan berbasis Recency, Frequency, dan Monetary menggunakan manual binning.
   - **Geospatial Analysis:** Pemetaan distribusi konsentrasi pesanan dan pelanggan berdasarkan negara bagian (*state*) di Brasil.

---

## 2. Struktur Direktori Proyek

```text
submission/
├───dashboard/
│   ├───main_data.csv          # Dataset teragregasi dan bersih untuk dashboard
│   └───dashboard.py           # Skrip aplikasi dashboard Streamlit
├───data/
│   ├───customers_dataset.csv
│   ├───geolocation_dataset.csv
│   ├───order_items_dataset.csv
│   ├───order_payments_dataset.csv
│   ├───order_reviews_dataset.csv
│   ├───orders_dataset.csv
│   ├───product_category_name_translation.csv
│   ├───products_dataset.csv
│   └───sellers_dataset.csv
├───notebook.ipynb             # Jupyter Notebook lengkap dan telah dieksekusi
├───README.md                  # Dokumentasi proyek
├───requirements.txt           # Daftar library dependensi Python
└───url.txt                    # Tautan dashboard Streamlit Cloud
```

---

## 3. Instalasi dan Setup Environment

### Langkah 1: Clone atau Buka Folder Proyek
Pastikan terminal berada pada direktori utama proyek (`submission`):
```bash
cd submission
```

### Langkah 2: Buat dan Aktifkan Virtual Environment (Opsional tapi Disarankan)
Menggunakan `venv` bawaan Python:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Atau menggunakan Conda:
```bash
conda create --name ecommerce-ds python=3.12
conda activate ecommerce-ds
```

### Langkah 3: Install Dependensi
Jalankan perintah berikut untuk menginstal seluruh pustaka yang diperlukan:
```bash
pip install -r requirements.txt
```

---

## 4. Cara Menjalankan

### A. Menjalankan Jupyter Notebook
Untuk meninjau seluruh tahapan data wrangling, EDA, visualisasi, dan kesimpulan:
```bash
jupyter notebook notebook.ipynb
```
Seluruh sel pada `notebook.ipynb` sudah dieksekusi dan menyertakan output visualisasi serta ringkasan insight.

### B. Menjalankan Dashboard Streamlit
Untuk menjalankan dashboard analitik interaktif di browser lokal:
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi dashboard akan otomatis terbuka di browser pada alamat default:
`http://localhost:8501`

---

## 5. Ringkasan Temuan & Rekomendasi Aksi

1. **Kategori Unggulan vs Underperforming:**
   - Kategori **bed_bath_table** (10.945 item) dan **health_beauty** (9.422 item) mencatatkan volume penjualan tertinggi. Kategori **health_beauty** menghasilkan total pendapatan terbesar (> 1,22 juta BRL).
   - Kategori dengan traksi paling rendah adalah **security_and_services** dan **fashion_childrens_clothes**.
   - *Rekomendasi:* Perbanyak promosi dan kemitraan seller pada kategori kesehatan dan kebutuhan rumah tangga, serta evaluasi katalog produk berkinerja rendah.

2. **Dampak Logistik terhadap Kepuasan Pelanggan:**
   - Pesanan tepat waktu memperoleh rata-rata review score **4.22/5.00** dengan lebih dari 60% rating bintang 5.
   - Pesanan terlambat anjlok ke rata-rata **2.60/5.00** dengan 55.9% pelanggan memberikan rating bintang 1.
   - *Rekomendasi:* Pengetatan SLA pengiriman bersama mitra ekspedisi dan penambahan estimasi kedatangan yang lebih realistis (*buffer time*).

3. **Segmentasi Pelanggan (RFM):**
   - Mayoritas basis pelanggan adalah pembeli satu kali yang masuk ke kelompok **Potential Regulars** dan **At Risk**.
   - *Rekomendasi:* Kirimkan kampanye email personalisasi dengan diskon ongkos kirim terbatas waktu kepada segmen *At Risk* untuk memicu repeat purchase.

4. **Konsentrasi Geografis:**
   - Wilayah Tenggara Brasil, terutama negara bagian **São Paulo (SP)**, mendominasi lebih dari 41% total pesanan nasional.
   - *Rekomendasi:* Prioritaskan penempatan hub logistik dan inventaris terdekat di kawasan SP untuk meminimalkan waktu tempuh dan menekan komplain pengiriman.
