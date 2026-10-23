import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Simulator BOK P2P Puskesmas 2027", layout="wide")

st.title("🛡️ Simulator Pagu & Peluang Capaian Target BOK P2P 2027")
st.markdown("Aplikasi Analisis Kelayakan Pagu Anggaran vs Target Fisik TOR untuk Sub-Jenis: **02-Surveilans, respons penyakit dan kesehatan lingkungan**")

st.divider()

# Master Menu P2P berdasarkan Dokumen Sosialisasi BOK 2027
MENU_P2P = {
    "01-Pelayanan Imunisasi termasuk penemuan kasus KIPI dan PD3I": {"satuan": "Laporan", "cap_default": 15},
    "02-Deteksi dini dan cek kesehatan gratis pemantauan dan tindak lanjut penyakit tidak menular": {"satuan": "Penduduk", "cap_default": 20},
    "03-Inspeksi kesling di Tempat dan Fasilitas Umum (TFU), Sarana Tempat Pengelolaan Pangan (TPP), Sarana Air Minum (SAM), Fasyankes": {"satuan": "Sarana", "cap_default": 5},
    "04-Penemuan kasus aktif dan pemantauan pengobatan TBC": {"satuan": "Kasus", "cap_default": 2},
    "05-Penemuan dan tindak lanjut kasus aktif penyakit menular": {"satuan": "Laporan", "cap_default": 10},
    "06-Penemuan Kasus Aktif Kusta dan komprofilaksis Kusta": {"satuan": "Laporan", "cap_default": 5},
    "08-Survei dan pengendalian vektor": {"satuan": "Laporan", "cap_default": 10},
    "09-Surveilans Kualitas Air Minum Rumah Tangga (KAMRT) dan Surveilans Kualitas Udara dalam Ruang": {"satuan": "Rumah tangga", "cap_default": 1},
    "10-Verifikasi sinyal/rumor, PE/pelacakan kontak penyakit berpotensi KLB/Wabah": {"satuan": "Laporan", "cap_default": 1},
    "11-Peningkatan Perubahan Perilaku Masyarakat (Pilar 1 dan 4 STBM)": {"satuan": "Desa/Kelurahan", "cap_default": 1}
}

# Sidebar Input Data
st.sidebar.header("📋 Input Parameter Kegiatan")
puskesmas_name = st.sidebar.text_input("Nama Puskesmas", "Puskesmas Pangkajene")

selected_menu = st.sidebar.selectbox("Pilih Rincian Kegiatan P2P", list(MENU_P2P.keys()))
satuan_output = MENU_P2P[selected_menu]["satuan"]

st.sidebar.subheader("💰 Alokasi Pagu & Biaya Operasional")
pagu_menu = st.sidebar.number_input("Pagu Anggaran Rincian Menu (Rp)", value=15000000, step=1000000, format="%d")
cost_per_visit = st.sidebar.number_input("Biaya Operasional per Kunjungan/Hari (Rp)", value=150000, step=10000, format="%d", help="Transport + Uang Harian (>8 jam) + Form")

st.sidebar.subheader("🎯 Target TOR & Kapasitas Lapangan")
target_tor = st.sidebar.number_input(f"Target Physical TOR ({satuan_output})", value=300, step=10)
cap_per_visit = st.sidebar.number_input(f"Estimasi {satuan_output} per Kunjungan Lapangan", value=MENU_P2P[selected_menu]["cap_default"], step=1)

# Logic Calculations
required_visits = math.ceil(target_tor / cap_per_visit) if cap_per_visit > 0 else 0
max_visits_budget = math.floor(pagu_menu / cost_per_visit) if cost_per_visit > 0 else 0
reachable_target = max_visits_budget * cap_per_visit
gap_target = max(0, target_tor - reachable_target)

success_rate = (reachable_target / target_tor * 100) if target_tor > 0 else 0
success_rate_capped = min(100.0, success_rate)

# Dashboard Main Panel
st.subheader(f"📍 Analisis: {puskesmas_name}")
st.caption(f"Rincian Menu: **{selected_menu}**")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Target TOR", f"{target_tor:,} {satuan_output}")
col2.metric("Kapasitas Kunjungan Pagu", f"{max_visits_budget} Kunjungan")
col3.metric("Estimasi Terjangkau", f"{reachable_target:,} {satuan_output}")
col4.metric("Peluang Capaian Target", f"{success_rate_capped:.1f}%")

st.divider()

# Progress Bar Visual
st.write("**Prosentase Keterjangkauan Target vs Anggaran BOK:**")
st.progress(int(success_rate_capped))

# Status Indicators
if success_rate_capped >= 100:
    st.success("✅ **STATUS: ANGGARAN AMAN** — Pagu BOK mencukupi untuk mendukung 100% target fisik TOR.")
elif success_rate_capped >= 75:
    st.warning(f"⚠️ **STATUS: PERLU EFISIENSI** — Pagu hanya mampu menjangkau {reachable_target} dari {target_tor} {satuan_output} (Defisit {gap_target} {satuan_output}). Disarankan integrasi kegiatan luar gedung.")
else:
    st.error(f"🚨 **STATUS: DEFISIT KRITIS** — Anggaran sangat kurang! Terdapat gap {gap_target} {satuan_output} yang tidak tercover BOK. Perlu penyesuaian target atau tambahan pagu.")

# Catatan Verifikasi Otomatis
st.subheader("📝 Catatan Rekomendasi Verifikator Kabupaten")
rec_text = (
    f"1. Untuk mencapai target TOR sebesar {target_tor} {satuan_output}, dibutuhkan minimal {required_visits} kali kunjungan/kegiatan lapangan.\n"
    f"2. Pagu yang dialokasikan (Rp{pagu_menu:,.0f}) hanya mampu membiayai {max_visits_budget} kali kunjungan.\n"
)
if gap_target > 0:
    needed_budget = (required_visits - max_visits_budget) * cost_per_visit
    rec_text += f"3. Diperlukan tambahan anggaran sebesar Rp{needed_budget:,.0f} atau optimasi biaya per kunjungan agar target tidak terancam drop."
else:
    rec_text += "3. Alokasi anggaran sudah efisien dan realistis."

st.info(rec_text)