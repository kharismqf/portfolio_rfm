import pandas as pd
import os
import numpy as np
from scipy import stats
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from PIL import Image

def project():
    # Judul utama harus di paling atas di dalam fungsi
    st.markdown("<h1 style='text-align: center;'>Analisis Segmentasi Pelanggan dengan RFM</h1>", unsafe_allow_html=True)

    # Load data
    data_path = ("GS Final.csv")
    try:
        data = pd.read_csv(data_path)
        st.success("Data berhasil dimuat!")
        st.dataframe(data)
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return

    # Penjelasan bisnis
    st.markdown("<h2 style='text-align: left;'>Business Understanding</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: justify;'>
    Global Superstore adalah perusahaan ritel global yang menjual berbagai macam produk, termasuk peralatan kantor, furnitur, dan perlengkapan teknologi, ke berbagai negara di dunia. Dataset ini mencakup informasi transaksi penjualan seperti pesanan, pelanggan, pengiriman, produk, hingga keuntungan yang dihasilkan. Dengan data yang kaya ini, perusahaan memiliki peluang besar untuk memahami perilaku pelanggan dan meningkatkan kinerja bisnis melalui strategi yang berbasis data.
    </div>
    """, unsafe_allow_html=True)

    # Tujuan bisnis
    st.markdown("<h2 style='text-align: left;'>Tujuan Bisnis</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: justify;'>
    Melakukan segmentasi pelanggan menggunakan analisis RFM (Recency, Frequency, Monetary) untuk memahami perilaku konsumen dan mengoptimalkan strategi pemasaran serta peningkatan profitabilitas. Untuk mencapai tujuan utama tersebut, beberapa tujuan spesifik yang akan dicapai adalah:
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <ul>
        <li>Mengidentifikasi jumlah dan distribusi pelanggan dalam setiap segmen</li>
        <li>Wilayah mana dengan performa terbaik berdasarkan jumlah pendapatan dan transaksi?</li>
        <li>Menilai distribusi penjualan berdasarkan kategori produk dan segmen pelanggan</li>
        <li>Bagaimana tren profit per segmen pelanggan setiap tahun? Apakah mengalami peningkatan?</li>
        <li>Bagaimana tren transaksi tiap kategori produk, serta kategori apa yang paling banyak penjualannya?</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: left;'>Tabel Deskripsi</h2>", unsafe_allow_html=True)

    st.markdown("""
    <table>
        <thead>
            <tr>
                <th>Kolom</th>
                <th>Tipe Data</th>
                <th>Deskripsi</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Row ID</td><td>int64</td><td>ID unik untuk tiap baris (mungkin hanya indeks)</td></tr>
            <tr><td>Order ID</td><td>object</td><td>ID unik untuk tiap pesanan</td></tr>
            <tr><td>Order Date</td><td>object</td><td>Tanggal pemesanan</td></tr>
            <tr><td>Ship Date</td><td>object</td><td>Tanggal pengiriman</td></tr>
            <tr><td>Ship Mode</td><td>object</td><td>Metode pengiriman (First Class, Standard, dll)</td></tr>
            <tr><td>Customer ID</td><td>object</td><td>ID unik pelanggan</td></tr>
            <tr><td>Customer Name</td><td>object</td><td>Nama pelanggan</td></tr>
            <tr><td>Segment</td><td>object</td><td>Segmen pelanggan (Consumer, Corporate, Home Office)</td></tr>
            <tr><td>City</td><td>object</td><td>Kota pelanggan</td></tr>
            <tr><td>State</td><td>object</td><td>Negara bagian atau provinsi pelanggan</td></tr>
            <tr><td>Country</td><td>object</td><td>Negara pelanggan</td></tr>
            <tr><td>Postal Code</td><td>float64</td><td>Kode pos pelanggan (banyak missing values)</td></tr>
            <tr><td>Market</td><td>object</td><td>Wilayah pasar geografis</td></tr>
            <tr><td>Region</td><td>object</td><td>Wilayah regional (APAC, EU, US, dll)</td></tr>
            <tr><td>Product ID</td><td>object</td><td>ID unik produk</td></tr>
            <tr><td>Category</td><td>object</td><td>Kategori produk (Furniture, Office Supplies, Technology)</td></tr>
            <tr><td>Sub-Category</td><td>object</td><td>Subkategori produk</td></tr>
            <tr><td>Product Name</td><td>object</td><td>Nama produk</td></tr>
            <tr><td>Sales</td><td>float64</td><td>Nilai penjualan dalam USD</td></tr>
            <tr><td>Quantity</td><td>int64</td><td>Jumlah unit yang dibeli</td></tr>
            <tr><td>Discount</td><td>float64</td><td>Diskon yang diberikan (misal 0.2 = 20%)</td></tr>
            <tr><td>Profit</td><td>float64</td><td>Keuntungan dari penjualan</td></tr>
            <tr><td>Shipping Cost</td><td>float64</td><td>Biaya pengiriman</td></tr>
            <tr><td>Order Priority</td><td>object</td><td>Prioritas pemesanan (Low, Medium, High, Critical)</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # Data Understanding
    st.markdown("<h2 style='text-align: left;'>Data Understanding</h2>", unsafe_allow_html=True)
    st.markdown("""
    <ul>
        <li>Dataset Global Superstore dari Kaggle, berfokus pada penjualan ritel</li>
        <li>Berisi detail transaksi, informasi pelanggan, dan kategori produk.</li>
        <li>Mencakup transaksi dari tahun 2011 hingga 2014 (sesuai dengan dataset Global Superstore).</li>
        <li>Memiliki 51.290 data transaksi dengan 24 kolom yang mencakup informasi pesanan, pelanggan, lokasi, hingga profitabilitas.</li>
    </ul>
    """, unsafe_allow_html=True)        


    # Data Preprocessing
    st.markdown("<h2 style='text-align: left;'>Data Preprocessing</h2>", unsafe_allow_html=True)

    if st.checkbox("1. Cek Duplikasi Data"):
        st.write("""Tidak ada duplikasi data
        """)

    if st.checkbox("2. Cek Missing Value"):
        st.write(""" Kolom “Postal Code” missing value 80%, maka drop kolom "Postal Code".        
        """)

    if st.checkbox("3. Data Manipulation"):
        st.write(""" Merubah format Order Date dan Ship Date ke datetime. Mengekstrak hari, bulan, dan tahun pada datetime. Merubah kolom kategorikal ke format ‘category’
        """)

    if st.checkbox("4. Cek Outlier"):
        st.write(""" Tidak ada outlier yang ekstrem
        """)

    # Customer Segmentation
    st.subheader('')
    with st.expander("Customer Segmentation"):
         st.write('## Tabel Customer Segmentation')
         st.markdown("""
            <table>
                <thead>
                    <tr>
                        <th>Nama Segment</th>
                        <th>Total Score</th>
                        <th>Deskripsi</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Gold</td><td>9</td><td>Sering melakukan transaksi, belanja dalam jumlah besar, dan merupakan pelanggan dengan nilai pembelian tertinggi.</td></tr>
                    <tr><td>Loyal</td><td>8</td><td>Memberikan kontribusi pendapatan yang baik, dan responsif terhadap promosi.</td></tr>
                    <tr><td>Promising</td><td>7</td><td>Pelanggan baru yang sudah mulai sering belanja dan dengan nilai pembelian cukup besar.</td></tr>
                    <tr><td>Regular</td><td>6</td><td>Pelanggan dengan nilai rata-rata dalam hal frekuensi, waktu terakhir belanja, dan nilai pembelian.</td></tr>
                    <tr><td>New Customer</td><td>6-7(recency days score 3)</td><td>Baru saja melakukan pembelian, tapi belum sering.</td></tr>
                    <tr><td>At Risk</td><td>6-7(recency days score 1)</td><td>Pernah melakukan pembelian besar dan cukup sering, namun sudah lama tidak kembali.</td></tr>
                    <tr><td>Fading</td><td>4&5</td><td>Memiliki nilai recency, frekuensi, dan pembelian di bawah rata-rata. Akan segera hilang jika tidak diaktivasi kembali.</td></tr>
                    <tr><td>Lost Customer</td><td>3</td><td>Skor paling rendah di semua aspek, lama tidak belanja, jarang, dan nilai kecil.</td></tr>
                    <tr><td>Unclassified</td><td><3</td><td>Tidak bisa dikelompokkan karena data yang tidak lengkap atau pola transaksi tidak memenuhi kriteria segmentasi.</td></tr>
                </tbody>
            </table>
            """, unsafe_allow_html=True)
         st.write('## RFM Quartil')
         image_path = (r"C:\Users\User\Pictures\Screenshot\Temuan&Hasil.png")
         image = Image.open(image_path)
         st.image(image, caption="RFM Quartil", use_container_width=True)

         st.write("## Analisis RFM Pelanggan")

         # Ubah format tanggal
         data['Order Date'] = pd.to_datetime(data['Order Date'])

         # Hitung nilai RFM
         rfm = data.groupby('Customer ID').agg({
            'Order Date': lambda x: (data['Order Date'].max() - x.max()).days,
            'Order ID': 'nunique',
            'Sales': 'sum'
         }).reset_index()

         rfm.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary']

         # Hitung skor RFM
         rfm['R_Score'] = pd.qcut(rfm['Recency'], 3, labels=[3, 2, 1]).astype(int)
         rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 3, labels=[1, 2, 3]).astype(int)
         rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 3, labels=[1, 2, 3]).astype(int)

         # Total RFM Score
         rfm['RFM_Score'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

         # Segmentasi pelanggan
         def segment(row):
            if row['RFM_Score'] == 9:
                return "Gold"
            elif row['RFM_Score'] == 8:
                return "Loyal"
            elif row['RFM_Score'] in [6, 7] and row['R_Score'] == 3:
                return "Promising"
            elif row['RFM_Score'] in [6, 7] and row['R_Score'] == 1:
                return "Regular"
            elif row['RFM_Score'] == 7:
                return "New Customer"
            elif row['RFM_Score'] == 6:
                return "At Risk"
            elif row['RFM_Score'] in [4, 5]:
                return "Fading"
            elif row['RFM_Score'] == 3:
                return "Lost Customer"
            else:
                return "Unclassified"
         rfm['Segment'] = rfm.apply(segment, axis=1)
         rfm.rename(columns={'Segment': 'rfm_segment'}, inplace=True)
         data = data.merge(rfm[['Customer ID', 'rfm_segment']], on='Customer ID', how='left')

         st.dataframe(rfm)


    # Penyelesaian Objektif Spesifik
    st.subheader('')
    with st.expander("Business Questions"):
         if st.checkbox("1. Wilayah dengan performa terbaik berdasarkan jumlah pendapatan dan transaksi"):
            # Buat ringkasan per Region
            region_summary = data.groupby('Region').agg({
                'Sales': 'sum',
                'Order ID': 'nunique'
            }).reset_index().rename(columns={'Sales': 'Total Sales', 'Order ID': 'Total Orders'})

            # Chart Total Sales per Region (diurutkan menurun)
            sales_sorted = region_summary.sort_values(by='Total Sales', ascending=True)  # ascending=True untuk bar horizontal dari bawah
            fig1 = px.bar(sales_sorted, 
                        x='Total Sales', 
                        y='Region', 
                        orientation='h',
                        title="Total Sales per Region (Descending)",
                        text_auto='.2s',
                        color='Total Sales',
                        color_continuous_scale='Plasma')
            st.plotly_chart(fig1)

            # Chart Total Orders per Region (diurutkan menurun)
            orders_sorted = region_summary.sort_values(by='Total Orders', ascending=True)
            fig2 = px.bar(orders_sorted, 
                        x='Total Orders', 
                        y='Region', 
                        orientation='h',
                        title="Total Orders per Region (Descending)",
                        text_auto=True,
                        color='Total Orders',
                        color_continuous_scale='Viridis')
            st.plotly_chart(fig2)

            st.write("### Insight:")
            st.markdown("""
            - Central jadi wilayah dengan performa terbaik (penjualan & transaksi tertinggi).
            - South & North juga menunjukkan performa tinggi, bisa jadi fokus pengembangan.
            - Canada & Caribbean merupakan wilayah dengan performa terendah.
            """)



         if st.checkbox("2. Distribusi penjualan berdasarkan kategori produk dan segmen pelanggan"):
            # Total penjualan berdasarkan Kategori Produk dan Segmen Pelanggan
            category_segment_sales = data.groupby(['Category', 'rfm_segment'])['Sales'].sum().unstack().fillna(0)

            st.write("### Distribusi Penjualan berdasarkan Kategori dan Segmen:")
            st.dataframe(category_segment_sales)

            # Visualisasi
            st.write("### Visualisasi Penjualan:")
            # Penjualan per kategori dan segmen
            category_segment_sales = data.groupby(['Category', 'rfm_segment'])['Sales'].sum().reset_index()
            fig3 = px.bar(category_segment_sales, x='Category', y='Sales', color='rfm_segment',
                        barmode='group', text_auto='.2s',
                        title='Penjualan berdasarkan Kategori Produk dan Segmen Pelanggan',
                        color_discrete_sequence=px.colors.qualitative.Vivid)
            st.plotly_chart(fig3)
            st.write("""
            Insight:
            1. X
            2. X
            """)

         if st.checkbox("3. Tren profit per segmen pelanggan setiap tahun"):
            # Pastikan tidak ada kolom rfm_segment sebelum merge
            if 'rfm_segment' in data.columns:
                data.drop(columns=['rfm_segment'], inplace=True)

            # Rename segment di RFM
            rfm.rename(columns={'Segment': 'rfm_segment'}, inplace=True)

            # Samakan tipe data untuk merge
            rfm['Customer ID'] = rfm['Customer ID'].astype(str)
            data['Customer ID'] = data['Customer ID'].astype(str)

            # Merge rfm segment ke data utama
            data = data.merge(rfm[['Customer ID', 'rfm_segment']], on='Customer ID', how='left')

            # Pastikan format tanggal
            data['Order Date'] = pd.to_datetime(data['Order Date'], errors='coerce')
            data['Year'] = data['Order Date'].dt.year

            # Debugging
            # st.write("Kolom setelah merge:", data.columns.tolist())
            # st.write("Cek NaN di rfm_segment:", data['rfm_segment'].isnull().sum())

            # Group by dan tampilkan hasil
            if data['rfm_segment'].isnull().all():
                st.error("Semua nilai 'rfm_segment' kosong setelah merge. Periksa 'Customer ID'.")
            else:
                profit_trend_rfm = data.groupby(['Year', 'rfm_segment'])['Profit'].sum().reset_index()
                st.dataframe(profit_trend_rfm)
                # Visualisasi Chart
                fig = px.bar(
                    profit_trend_rfm,
                    y='Year',
                    x='Profit',
                    color='rfm_segment',
                    orientation='h',
                    title='Tren Profit per Segment Pelanggan Tiap Tahun (Horizontal)',
                    text_auto='.2s'
                    )
                st.plotly_chart(fig, use_container_width=True)
            st.write("""
            Insight:
            1. X
            2. X
            """)

         if st.checkbox("4. Tren transaksi tiap kategori produk, serta kategori apa yang paling banyak penjualannya"):
            # Pastikan format datetime
            data['Order Date'] = pd.to_datetime(data['Order Date'])
            data['Month'] = data['Order Date'].dt.to_period("M").dt.to_timestamp()

            # Ambil batas bulan terendah dan tertinggi
            min_month = data["Month"].min().to_pydatetime()
            max_month = data["Month"].max().to_pydatetime()


            # Konversi ke datetime untuk slider
            start_date, end_date = st.slider(
                "Pilih Rentang Bulan",
                min_value=min_month,
                max_value=max_month,
                value=(min_month, max_month),
                format="MMM YYYY"
            )

            # Filter data berdasarkan slider
            filtered_data = data[(data["Month"] >= start_date) & (data["Month"] <= end_date)]

            # Hitung jumlah order per bulan per kategori
            monthly_trend = filtered_data.groupby(["Month", "Category"])["Order ID"].nunique().reset_index()
            monthly_trend.rename(columns={"Order ID": "Total Orders"}, inplace=True)

            # Plot line chart
            fig = px.line(
                monthly_trend,
                x="Month",
                y="Total Orders",
                color="Category",
                markers=True,
                title="📊 Tren Jumlah Transaksi Bulanan per Kategori Produk",
                labels={"Month": "Bulan", "Total Orders": "Jumlah Transaksi", "Category": "Kategori Produk"},
            )

            fig.update_traces(mode="lines+markers", textposition="top center")
            fig.update_layout(hovermode="x unified")

            st.plotly_chart(fig, use_container_width=True)

            # Total penjualan per kategori
            total_sales_category = data.groupby('Category')['Sales'].sum().sort_values(ascending=False)
            st.write("###### Total Penjualan per Kategori Produk:")
            st.dataframe(total_sales_category)
            # Transaksi per kategori per tahun
            category_yearly = data.groupby([data['Year'], 'Category'])['Order ID'].nunique().reset_index()
            category_yearly.columns = ['Year', 'Category', 'Total Orders']

            # Total penjualan per kategori
            total_sales_category = data.groupby('Category')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False)

            fig6 = px.pie(total_sales_category, values='Sales', names='Category', hole=0.4,
                        title="Proporsi Penjualan Tiap Kategori", color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig6)
            st.write("""
            Insight:
            1. X
            2. X
            """)

    st.subheader('Rekomendasi Bisnis')
    st.markdown("""
            **1. Reaktivasi Pelanggan Tidak Aktif untuk Mengurangi Potensi Churn**
            
            **🎯 Target**: Segmen *Fading*, *At-Risk*, dan *Lost*
            
            **📌 Strategi:**
            - **Reaktivasi Melalui Penawaran Personal**  
            Kirim diskon personal kepada pelanggan yang lama tidak bertransaksi, terutama yang dulunya aktif (*Fading*).
            - **Trigger Email Berdasarkan Recency**  
            Kirim reminder otomatis ke pelanggan dengan *recency* > 60 hari.
            - **Re-engagement Campaign Khusus Segmen Lost**  
            Berikan benefit khusus (seperti cashback atau hadiah) kepada pelanggan *Lost* agar mencoba kembali platform.
            """)
    st.markdown("""
            **2. Maksimalkan Potensi Segmen Loyal & Aktif untuk Mendorong Revenue**
            
            **🎯 Target**: Loyal, Gold, dan Promising Customers
            
            **📌 Strategi:**
            - **Loyalty Program Eksklusif**
            Buat program loyalitas berbasis level untuk segmen top-tier seperti Loyal.
            - **Early Access & Eksklusivitas**
            Berikan akses awal pada produk baru atau diskon terbatas untuk menjaga rasa eksklusif.

            """)
    st.markdown("""
            **3. Fokus pada Wilayah dengan Volume Tinggi tapi Performa Belum Optimal**
            
            **🎯 Target**: Central, South, dan North
            
            **📌 Strategi:**
            - Pertahankan Central melalui program loyalitas & upselling produk.
            - Dorong pertumbuhan South & North lewat promosi dan perluasan distribusi.
            - Evaluasi wilayah lemah (Canada & Caribbean) dan sesuaikan strategi pemasaran.
            """)
    st.markdown("""
            **4. Tingkatkan Profitabilitas dari Kategori Produk Terbaik**
            
            **🎯 Target**: Office Supplies, Technology, Furniture
            
            **📌 Strategi:**
            - **Office Supplies** → Buat program langganan bulanan untuk pelanggan B2B atau instansi.
            - **Technology** → Bundling produk dengan aksesori atau garansi tambahan untuk mendorong nilai transaksi.
            - **Furniture** → Tawarkan promo musiman untuk mendorong pembelian produk dengan margin besar.
            """)
if __name__ == "__main__":
    project()
