import streamlit as st
import math

st.set_page_config(page_title="Simulator BOK - Deteksi Dini PTM Pangkep", layout="wide")

st.title("🩺 Simulator Pagu & Target: Deteksi Dini & Cek Kesehatan Gratis (CKG) PTM")
st.markdown("Alat analisis kesesuaian pagu anggaran BOK Puskesmas berdasarkan data resmi 23 Puskesmas Kabupaten Pangkep.")

st.divider()

# Daftar Resmi 23 Puskesmas Kabupaten Pangkep sesuai data
LIST_PUSKESMAS = [
    "Kota Pangkajene",
    "Bonto Perak",
    "Minasa Te'ne",
    "Kalabbirang",
    "Bungoro",
    "Bowong Cindea",
    "Labakkang",
    "Pundata Baji",
    "Ma'rang",
    "Taraweang",
    "Padang Lampe",
    "Segeri",
    "Baring",
    "Mandalle",
    "Balocci",
    "Bantimala",
    "Lk. Tupabbiring",
    "Sabutung",
    "Sarappo",
    "Lk. Tangaya",
    "Sailus",
    "Lk. Kalmas",
    "Pammantauang"
]

# Sidebar Parameter Khusus PTM dengan Dropdown 23 Puskesmas
st.sidebar.header("📋 Parameter Kegiatan PTM")
puskesmas_name = st.sidebar.selectbox("Pilih Nama Puskesmas", LIST_PUSKESMAS)

st.sidebar.subheader("💰 Anggaran & Biaya Tim")
pagu_menu = st.sidebar.number_input("Pagu Anggaran Menu CKG/PTM (Rp)", value=20000000, step=1000000, format="%d")
transport_per_orang = st.sidebar.number_input("Biaya (Transport + Uang Harian) per Orang (Rp)", value=150000, step=10000, format="%d")
jumlah_petugas = st.sidebar.slider("Jumlah Petugas Sekali Turun Lapangan (Orang)", min_value=1, max_value=10, value=5)

# Kalkulasi total biaya per 1 kali kegiatan/kunjungan tim
total_cost_per_visit = transport_per_orang * jumlah_petugas

st.sidebar.subheader("🎯 Target Sasaran & Kapasitas")
target_penduduk = st.sidebar.number_input("Target Penduduk Menerima Layanan CKG/PTM (Orang)", value=1000, step=50)
kapasitas_per_kunjungan = st.sidebar.number_input("Rata-rata Orang Dilayani per 1 Kali Kegiatan", value=25, step=1)

# Kalkulasi Logika
required_visits = math.ceil(target_penduduk / kapasitas_per_kunjungan) if kapasitas_per_kunjungan > 0 else 0
max_visits_budget = math.floor(pagu_menu / total_cost_per_visit) if total_cost_per_visit > 0 else 0
reachable_population = max_visits_budget * kapasitas_per_kunjungan
gap_population = max(0, target_penduduk - reachable_population)

success_rate = (reachable_population / target_penduduk * 100) if target_penduduk > 0 else 0
success_rate_capped = min(100.0, success_rate)

# Dashboard Utama
st.subheader(f"📍 Hasil Analisis PTM: Puskesmas {puskesmas_name}")
st.info(f"💡 Konfigurasi Tim: **{jumlah_petugas} orang petugas** per turun lapangan. Total biaya per 1 kegiatan = **Rp{total_cost_per_visit:,}**")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Target Sasaran TOR", f"{target_penduduk:,} Penduduk")
col2.metric("Kapasitas Kunjungan Pagu", f"{max_visits_budget} Kunjungan")
col3.metric("Penduduk Terjangkau", f"{reachable_population:,} Penduduk")
col4.metric("Peluang Capaian Target", f"{success_rate_capped:.1f}%")

st.divider()

# Progress Bar
st.write("**Tingkat Ketercapaian Target Sasaran CKG/PTM:**")
st.progress(int(success_rate_capped))

# Status Analisis
if success_rate_capped >= 100:
    st.success("✅ **STATUS: AMAN** — Pagu anggaran mencukupi untuk mencapai 100% target penduduk skrining PTM dengan format tim tersebut.")
elif success_rate_capped >= 75:
    st.warning(f"⚠️ **STATUS: MODERAT** — Pagu belum sepenuhnya mencakup target. Terdapat defisit sekitar **{gap_population} penduduk**. Perlu efisiensi jumlah personil atau integrasi kegiatan.")
else:
    st.error(f"🚨 **STATUS: DEFISIT KRITIS** — Dengan tim {jumlah_petugas} orang, pagu cepat habis! Sebanyak **{gap_population} penduduk** tidak tercover anggaran.")

# Catatan Rekomendasi Verifikator
st.subheader("📝 Catatan Rekomendasi untuk Verifikasi TOR/RAB")
rec_text = (
    f"1. Berdasarkan target TOR ({target_penduduk} penduduk) dengan kapasitas {kapasitas_per_kunjungan} orang/kegiatan di **Puskesmas {puskesmas_name}**, "
    f"diperlukan minimal **{required_visits} kali kunjungan lapangan**.\n"
    f"2. Mengingat sekali turun melibatkan **{jumlah_petugas} orang** (biaya per turun Rp{total_cost_per_visit:,.0f}), "
    f"pagu Rp{pagu_menu:,.0f} hanya sanggup membiayai **{max_visits_budget} kali kunjungan**.\n"
)
if gap_population > 0:
    extra_budget = (required_visits - max_visits_budget) * total_cost_per_visit
    rec_text += f"3. Solusi Verifikasi: Tambahan pagu sebesar **Rp{extra_budget:,.0f}**, atau lakukan penyesuaian jumlah tim (misal dari {jumlah_petugas} orang menjadi 3-4 orang) agar frekuensi kunjungan bisa lebih banyak."
else:
    rec_text += "3. Alokasi anggaran dan komposisi tim sudah seimbang."

st.info(rec_text)