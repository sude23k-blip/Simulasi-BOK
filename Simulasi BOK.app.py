import streamlit as st
import math

st.set_page_config(page_title="Simulator BOK - Deteksi Dini PTM", layout="wide")

st.title("🩺 Simulator Pagu & Target: Deteksi Dini & Cek Kesehatan Gratis (CKG) PTM")
st.markdown("Alat analisis kesesuaian antara pagu anggaran BOK Puskesmas dengan target sasaran penduduk untuk skrining PTM.")

st.divider()

# Sidebar Parameter Khusus PTM
st.sidebar.header("📋 Parameter Kegiatan PTM")
puskesmas_name = st.sidebar.text_input("Nama Puskesmas", "Puskesmas Pangkajene")

st.sidebar.subheader("💰 Anggaran & Biaya")
pagu_menu = st.sidebar.number_input("Pagu Anggaran Menu CKG/PTM (Rp)", value=20000000, step=1000000, format="%d")
cost_per_visit = st.sidebar.number_input("Biaya Operasional per Kunjungan Tim (Rp)", value=150000, step=10000, format="%d", help="Transport + Uang Harian + Penggandaan Form")

st.sidebar.subheader("🎯 Target Sasaran & Kapasitas")
target_penduduk = st.sidebar.number_input("Target Penduduk Menerima Layanan CKG/PTM (Orang)", value=1000, step=50)
kapasitas_per_kunjungan = st.sidebar.number_input("Rata-rata Orang Dilayani per 1 Kali Kunjungan/Posyandu", value=25, step=1)

# Kalkulasi Logika
required_visits = math.ceil(target_penduduk / kapasitas_per_kunjungan) if kapasitas_per_kunjungan > 0 else 0
max_visits_budget = math.floor(pagu_menu / cost_per_visit) if cost_per_visit > 0 else 0
reachable_population = max_visits_budget * kapasitas_per_kunjungan
gap_population = max(0, target_penduduk - reachable_population)

success_rate = (reachable_population / target_penduduk * 100) if target_penduduk > 0 else 0
success_rate_capped = min(100.0, success_rate)

# Dashboard Utama
st.subheader(f"📍 Hasil Analisis PTM: {puskesmas_name}")

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
    st.success("✅ **STATUS: AMAN** — Pagu anggaran mencukupi untuk mencapai 100% target penduduk skrining PTM.")
elif success_rate_capped >= 75:
    st.warning(f"⚠️ **STATUS: MODERAT** — Pagu belum sepenuhnya mencakup target. Terdapat defisit sekitar **{gap_population} penduduk**. Disarankan mengintegrasikan CKG ke dalam kegiatan Posyandu rutin.")
else:
    st.error(f"🚨 **STATUS: DEFISIT KRITIS** — Pagu sangat kurang! Sebanyak **{gap_population} penduduk** tidak tercover anggaran. Perlu penyesuaian target atau penambahan alokasi pagu.")

# Catatan Rekomendasi Verifikator
st.subheader("📝 Catatan Rekomendasi untuk Verifikasi TOR/RAB")
rec_text = (
    f"1. Berdasarkan target TOR ({target_penduduk} penduduk) dengan kapasitas pelayanan rata-rata {kapasitas_per_kunjungan} orang/kegiatan, "
    f"diperlukan minimal **{required_visits} kali kegiatan/kunjungan lapangan**.\n"
    f"2. Pagu yang tersedia sebesar **Rp{pagu_menu:,.0f}** hanya mampu membiayai **{max_visits_budget} kali kunjungan**.\n"
)
if gap_population > 0:
    extra_budget = (required_visits - max_visits_budget) * cost_per_visit
    rec_text += f"3. Agar target tercapai penuh tanpa defisit, dibutuhkan tambahan anggaran sekitar **Rp{extra_budget:,.0f}** atau optimalisasi titik kumpul skrining."
else:
    rec_text += "3. Alokasi anggaran untuk Deteksi Dini PTM sudah efisien dan proporsional."

st.info(rec_text)