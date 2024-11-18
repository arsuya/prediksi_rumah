import streamlit as st
import pandas as pd
from joblib import load

# Load model yang sudah disimpan
model = load('model_depok.joblib')

# Judul aplikasi
st.title("Prediksi Harga Rumah Bekas di Depok")

# Deskripsi aplikasi
st.markdown("""
Aplikasi ini akan membantu Anda memprediksi harga rumah bekas di Depok berdasarkan beberapa fitur seperti jumlah kamar tidur, luas tanah, luas bangunan, sertifikat, dan lokasi.
""")

# Input data dari pengguna
st.header("Masukkan Informasi Rumah")

# Input angka untuk fitur numerik tanpa min_value dan max_value
kamar_tidur = st.number_input("Jumlah Kamar Tidur", value=3)
luas_tanah = st.number_input("Luas Tanah (m²)", value=100)
luas_bangunan = st.number_input("Luas Bangunan (m²)", value=80)

# Input untuk fitur kategorikal
sertifikat_options = ['Sertifikat Hak Milik', 'Hak Guna Bangunan']
sertifikat = st.selectbox("Jenis Sertifikat", sertifikat_options)

lokasi_options = ['Beji', 'Bojongsari', 'Cilodong', 'Cimanggis', 'Cinere', 'Cipayung', 'Limo', 'Pancoran Mas', 'Sawangan', 'Sukmajaya', 'Tapos']
lokasi = st.selectbox("Lokasi", lokasi_options)

# Convert input ke dalam dataframe
input_data = pd.DataFrame({
    'kamar_tidur': [kamar_tidur],
    'luas_tanah': [luas_tanah],
    'luas_bangunan': [luas_bangunan],
    'sertifikat': [sertifikat],
    'lokasi': [lokasi]
})

# Fungsi untuk format harga
def format_harga(harga):
    if harga >= 1_000_000_000:  # Lebih dari atau sama dengan 1 miliar
        return f"Rp {harga/1_000_000_000:.1f} M"
    elif harga >= 1_000_000:  # Lebih dari atau sama dengan 1 juta
        return f"Rp {harga/1_000_000:.0f} Jt"
    else:  # Kurang dari 1 juta
        return f"Rp {harga:,.2f}"

# Prediksi harga rumah berdasarkan input
if st.button("Prediksi Harga Rumah"):
    # Lakukan prediksi menggunakan model
    prediksi_harga = model.predict(input_data)[0]

    # Tentukan rentang harga dengan 40% margin
    rentang = prediksi_harga * 0.1
    rentang_bawah = prediksi_harga - rentang
    rentang_atas = prediksi_harga + rentang

    # Format rentang harga
    rentang_bawah_format = format_harga(rentang_bawah)
    rentang_atas_format = format_harga(rentang_atas)

    # Tampilkan rentang harga
    st.subheader(f"Rentang Harga Rumah: {rentang_bawah_format} - {rentang_atas_format}")

# Tampilan Footer
st.markdown("""
---
Developed by Arvin Surya Wibowo
""")
