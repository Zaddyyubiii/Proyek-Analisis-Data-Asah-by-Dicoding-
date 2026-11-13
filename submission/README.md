# Proyek Analisis Data: E-Commerce Public Dataset

Proyek akhir analisis data kelas **Belajar Analisis Data dengan Python** dari Dicoding Indonesia. Proyek ini mencakup seluruh tahapan analisis data secara komprehensif: perumusan pertanyaan bisnis berstandar SMART, Data Wrangling (Gathering, Assessing, Cleaning), Exploratory Data Analysis (EDA), Visualisasi Data interaktif, Analisis Lanjutan (RFM Analysis & Geospatial Analysis interaktif dengan Folium), serta Dashboard Analitik Interaktif berbasis Streamlit.

---

## 1. Pertanyaan Bisnis (SMART Method)
1. **Performa Kategori Produk & Penjualan (2017–2018):**
   *Kategori produk apa saja yang mencatatkan volume penjualan (jumlah item terjual) dan pendapatan (revenue) tertinggi serta terendah sepanjang tahun 2017 sampai 2018?*
2. **Kualitas Pengiriman & Kepuasan Pelanggan (2017–2018):**
   *Bagaimana korelasi dan perbedaan rata-rata skor ulasan (customer review score) antara pesanan tepat waktu (On Time) dan pesanan terlambat (Late) pada transaksi tahun 2017 sampai 2018?*
3. **Penerapan Analisis Lanjutan (Kriteria Bintang 5):**
   - **RFM Analysis:** Mengelompokkan pelanggan berdasarkan perilaku transaksi (*Recency*, *Frequency*, *Monetary*) menggunakan segmentasi *manual grouping* tanpa algoritma machine learning.
   - **Geospatial Analysis:** Menganalisis sebaran spasial pelanggan dan penjual di Brasil menggunakan peta interaktif **Folium** berbasis koordinat latitude dan longitude.

---

## 2. Struktur Direktori Proyek

```text
submission/
├───dashboard/
│   ├───main_data.csv          # Dataset teragregasi dan bersih untuk dashboard
│   ├───dashboard.py           # Skrip aplikasi dashboard Streamlit interaktif
│   └───requirements.txt       # Dependensi dashboard
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
└───url.txt                    # Tautan dashboard Streamlit Community Cloud
```

---

## 3. Instalasi dan Setup Environment

### Langkah 1: Masuk ke Direktori Proyek
```bash
cd submission
```

### Langkah 2: Buat dan Aktifkan Virtual Environment (Opsional)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Langkah 3: Install Dependensi
```bash
pip install -r requirements.txt
```

---

## 4. Cara Menjalankan

### A. Menjalankan Jupyter Notebook
```bash
jupyter notebook notebook.ipynb
```
Seluruh sel pada `notebook.ipynb` sudah dieksekusi lengkap dan menyertakan output visualisasi, tabel statistik, pengujian korelasi, serta peta interaktif Folium.

### B. Menjalankan Dashboard Streamlit
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi dashboard akan otomatis terbuka di browser lokal pada alamat default:
`http://localhost:8501`

---

## 5. Ringkasan Temuan Kuantitatif & Rekomendasi Aksi

### A. Performa Produk & Penjualan (Pertanyaan 1)
- **Top Performers:**
  - Volume Tertinggi: `bed_bath_table` (**10.945 item**, revenue: R$ 1.022.955,77), `health_beauty` (**9.422 item**, revenue: R$ 1.229.557,50), dan `sports_leisure` (**8.413 item**, revenue: R$ 952.661,40).
  - Revenue Tertinggi: `health_beauty` (**R$ 1.229.557,50**, 9.422 item), `watches_gifts` (**R$ 1.163.187,91**, 5.853 item), dan `bed_bath_table` (**R$ 1.022.955,77**, 10.945 item).
- **Lowest Performers:**
  - Volume Terendah: `security_and_services` (**2 item**, revenue: R$ 283,29), `fashion_childrens_clothes` (**7 item**, revenue: R$ 519,95), dan `la_cuisine` (**14 item**, revenue: R$ 2.054,99).
  - Revenue Terendah: `security_and_services` (**R$ 283,29**, 2 item), `fashion_childrens_clothes` (**R$ 519,95**, 7 item), dan `cds_dvds_musicals` (**R$ 730,00**, 14 item).
- **Pembedaan Karakteristik:** Kategori volume terendah belum tentu memiliki pendapatan terendah. Contohnya, `la_cuisine` berada di posisi ke-3 terbawah volume (14 item), namun mencetak revenue R$ 2.054,99 karena harga satuan produknya tinggi (rata-rata R$ 146,78). Sebaliknya, `home_comfort_2` menjual 30 item namun revenue-nya hanya R$ 760,27 karena harga rata-ratanya hanya R$ 25,34.

### B. Kepuasan Pelanggan & Logistik (Pertanyaan 2)
- **Konteks Transaksi:** Dari **96.203 pesanan** pada periode 2017–2018, sebanyak **88.381 pesanan (91,87%)** tiba tepat waktu (*On Time*), sedangkan **7.822 pesanan (8,13%)** mengalami keterlambatan (*Late*).
- **Penurunan Skor Ulasan:** Pesanan tepat waktu memperoleh rata-rata skor ulasan **4,22/5,00** (std: 1,23), sementara pesanan terlambat anjlok ke **2,60/5,00** (std: 1,68). Terjadi penurunan skor sebesar **1,62 poin**, dengan dasar perhitungan persentase:
  $$\% \text{ Penurunan} = \frac{4{,}22 - 2{,}60}{4{,}22} \times 100\% = 38{,}25\%$$
- **Pengukuran Korelasi Statistik:** Uji korelasi Pearson menunjukkan korelasi negatif yang signifikan antara keterlambatan dengan skor ulasan ($r = -0{,}3588, p < 0{,}001$), serta antara durasi keterlambatan hari dengan skor ulasan ($r = -0{,}2643, p < 0{,}001$).
- **Interpretasi Objektif:** Data membuktikan adanya hubungan asosiatif negatif yang kuat di mana pesanan terlambat cenderung mendapatkan ulasan buruk (45,80% rating bintang 1 pada pesanan terlambat vs 8,29% pada pesanan tepat waktu). Temuan ini tidak diklaim sebagai hubungan sebab-akibat tunggal, karena kepuasan pelanggan juga dipengaruhi oleh kualitas produk dan respon komunikasi seller.

### C. Analisis Lanjutan (RFM & Geospatial Folium)
- **RFM:** Sebagian besar pelanggan merupakan pembeli satu kali yang berada pada segmen *Potential Regulars* (38.835) dan *At Risk* (29.231).
- **Geospasial:** Peta interaktif Folium mengidentifikasi konsentrasi ekstrem aktivitas e-commerce di wilayah pesisir Tenggara Brasil (São Paulo >41% pesanan nasional). Konsentrasi penjual (*sellers*) di kawasan Tenggara menghasilkan rata-rata ongkos kirim yang jauh lebih murah (R$ 15,15 di SP vs R$ 38,26 di MA).

---

## 6. Rekomendasi Bisnis (Action Items)

1. **Pengelolaan Stok Cadangan (*Safety Stock*):**
   Menerapkan kebijakan *safety stock* otomatis sebesar 15–20% di atas rata-rata volume bulanan untuk kategori unggulan (*Bed Bath Table* dan *Health Beauty*) menjelang periode kampanye besar (seperti Black Friday dan akhir tahun) guna mencegah kehabisan stok (*stock-out*).
2. **Strategi Promosi & Bundling:**
   Merancang program promosi *bundling* antara kategori bervolume tinggi (*Bed Bath Table*) dengan kategori bernilai transaksi tinggi seperti *Watches Gifts* (rata-rata R$ 198,73) guna meningkatkan *Average Order Value*.
3. **Evaluasi & Restrukturisasi Kategori Terendah:**
   Mengaudit kategori berkinerja terendah (*Security & Services*, *Fashion Childrens Clothes*, *CDS DVDS Musicals*), mengevaluasi listing merchant, meningkatkan relevansi pencarian, atau merelokasi slot promosi ke kategori yang lebih diminati pasar.
4. **Audit Pengiriman & Pengetatan SLA Logistik:**
   Mengevaluasi performa pengiriman pada 7.822 pesanan terlambat dan memberlakukan Service Level Agreement (SLA) ketat dengan penalti performa bagi mitra ekspedisi yang gagal mencapai target ketepatan waktu 95% pada rute antar-kawasan.
5. **Estimasi Waktu Pengiriman Dinamis (*Dynamic EDD*):**
   Memperbaiki penetapan estimasi tanggal kedatangan dengan menyematkan *buffer time* 2–3 hari kerja untuk wilayah di luar Tenggara, agar ekspektasi pelanggan tetap realistis.
6. **Sistem Notifikasi Dini & Pemulihan Proaktif:**
   Membangun sistem pelacakan otomatis yang mendeteksi paket tertahan di hub transit lebih dari 48 jam untuk mengirimkan permohonan maaf dan voucher diskon belanja berikutnya secara proaktif sebelum pelanggan memberikan ulasan buruk.
