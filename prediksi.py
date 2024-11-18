import streamlit as st
import pandas as pd
from joblib import load

# Load model yang sudah disimpan
model = load('model_depok.joblib')

# Judul aplikasi dengan tampilan lebih menarik
st.title("🏡 Prediksi Harga Rumah Second di Depok")

# Deskripsi aplikasi
st.markdown("""
Selamat datang di aplikasi prediksi harga rumah second di Depok! 
Masukkan informasi rumah yang ingin kamu prediksi harganya, dan kami akan memberikan perkiraan harga lengkap dengan rentang harga yang bisa kamu pertimbangkan.
""")

# Styling header dan teks
st.markdown("""
<style>
    .st-header {
        font-size: 30px;
        font-weight: bold;
        color: #2E3B4E;
    }
    .st-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-size: 18px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
    }
    .st-button:hover {
        background-color: #45a049;
    }
    .st-subheader {
        font-size: 22px;
        color: #444;
    }
</style>
""", unsafe_allow_html=True)

# Input data dari pengguna
st.header("Masukkan Info Rumah Kamu")

# Input angka untuk fitur numerik tanpa min_value dan max_value
kamar_tidur = st.number_input("Jumlah Kamar Tidur", value=3, step=1)
luas_tanah = st.number_input("Luas Tanah (m²)", value=100, step=1)
luas_bangunan = st.number_input("Luas Bangunan (m²)", value=80, step=1)

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
if st.button("Prediksi Harga Rumah", key="predict_btn"):
    # Lakukan prediksi menggunakan model
    prediksi_harga = model.predict(input_data)[0]

    # Tentukan rentang harga dengan 10% margin
    rentang = prediksi_harga * 0.1  # 10% margin untuk rentang harga
    rentang_bawah = prediksi_harga - rentang
    rentang_atas = prediksi_harga + rentang

    # Format rentang harga
    rentang_bawah_format = format_harga(rentang_bawah)
    rentang_atas_format = format_harga(rentang_atas)

    # Tampilkan rentang harga
    st.subheader(f"Rentang Harga Rumah: {rentang_bawah_format} - {rentang_atas_format}")

# Tampilan Footer dengan gaya santai
st.markdown("""
---
Ini adalah aplikasi prediksi harga rumah, semoga membantu! 😄
Developed by Arvin Surya Wibowo
""", unsafe_allow_html=True)
