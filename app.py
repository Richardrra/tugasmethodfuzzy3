import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. KONFIGURASI HALAMAN & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="Fuzzy Kelayakan Beasiswa", layout="wide")

# Custom CSS untuk UI/UX yang lebih modern dan bersih
st.markdown("""
    <style>
    /* Menyembunyikan menu hamburger dan footer bawaan agar tidak clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Background aplikasi dengan gradasi sangat halus */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Styling untuk Metric Card (Kotak Nilai) */
    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 15px;
        padding: 15px 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #4CAF50;
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Styling khusus Tab agar terlihat seperti tombol modern */
    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 20px !important;
    }
    
    /* Kustomisasi kontainer utama */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Mempercantik box info/success */
    .stAlert {
        border-radius: 12px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HEADER & INPUT SIDEBAR
# ==========================================
st.title(" Logika Fuzzy: Kelayakan Beasiswa")
st.markdown("Implementasi penentuan kelayakan beasiswa berdasarkan **Indeks Prestasi Kumulatif (IPK)** dengan antarmuka yang diperbarui.")

st.sidebar.header(" Parameter Input")
st.sidebar.write("Geser *slider* untuk mengatur nilai IPK mahasiswa:")
x_input = st.sidebar.slider("Nilai IPK:", min_value=0.00, max_value=4.00, value=3.10, step=0.01)

# ==========================================
# 3. FUNGSI MATEMATIKA FUZZIFIKASI
# ==========================================
def mu_tidak_layak(x):
    if x <= 1.5: return 1.0
    elif 1.5 < x < 2.5: return (2.5 - x) / 1.0
    else: return 0.0

def mu_dipertimbangkan(x):
    if x <= 1.5 or x >= 3.5: return 0.0
    elif 1.5 < x < 2.5: return (x - 1.5) / 1.0
    else: return (3.5 - x) / 1.0

def mu_layak(x):
    if x <= 2.5: return 0.0
    elif 2.5 < x < 3.5: return (x - 2.5) / 1.0
    else: return 1.0

val_tidak_layak = mu_tidak_layak(x_input)
val_dipertimbangkan = mu_dipertimbangkan(x_input)
val_layak = mu_layak(x_input)

# ==========================================
# 4. TAB KONTEN UTAMA
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Fungsi Keanggotaan", 
    "Perhitungan Derajat Keanggotaan", 
    "Grafik Himpunan Fuzzy", 
    "Interpretasi Hasil"
])

with tab1:
    st.header("Fungsi Keanggotaan (\u03bc)")
    st.write("Representasi matematis dari himpunan fuzzy (Domain 0.00 - 4.00):")
    
    st.markdown("**1. Himpunan Tidak Layak**")
    st.latex(r'''
    \mu_{\text{Tidak Layak}}(x) = 
    \begin{cases} 
    1, & x \le 1.5 \\
    \frac{2.5 - x}{1.0}, & 1.5 < x < 2.5 \\
    0, & x \ge 2.5 
    \end{cases}
    ''')
    
    st.markdown("**2. Himpunan Dipertimbangkan**")
    st.latex(r'''
    \mu_{\text{Dipertimbangkan}}(x) = 
    \begin{cases} 
    0, & x \le 1.5 \text{ atau } x \ge 3.5 \\
    \frac{x - 1.5}{1.0}, & 1.5 < x < 2.5 \\
    \frac{3.5 - x}{1.0}, & 2.5 \le x < 3.5 
    \end{cases}
    ''')

    st.markdown("**3. Himpunan Layak**")
    st.latex(r'''
    \mu_{\text{Layak}}(x) = 
    \begin{cases} 
    0, & x \le 2.5 \\
    \frac{x - 2.5}{1.0}, & 2.5 < x < 3.5 \\
    1, & x \ge 3.5 
    \end{cases}
    ''')

with tab2:
    st.header("Perhitungan Derajat Keanggotaan")
    st.write(f"Hasil fuzzifikasi untuk nilai IPK = **{x_input:.2f}**:")
    
    # Karena sudah ada CSS, metrik ini akan tampil dalam bentuk kartu putih yang rapi
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="μ Tidak Layak", value=f"{val_tidak_layak:.2f}")
    col_b.metric(label="μ Dipertimbangkan", value=f"{val_dipertimbangkan:.2f}")
    col_c.metric(label="μ Layak", value=f"{val_layak:.2f}")

with tab3:
    st.header("Grafik Himpunan Fuzzy")
    
    x_vals = np.linspace(0, 4, 500)
    y_tidak_layak = [mu_tidak_layak(x) for x in x_vals]
    y_dipertimbangkan = [mu_dipertimbangkan(x) for x in x_vals]
    y_layak = [mu_layak(x) for x in x_vals]
    
    # Mengatur background grafik agar transparan dan membaur dengan background web
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    ax.plot(x_vals, y_tidak_layak, label="Tidak Layak", color="#ff4b4b", linewidth=2.5)
    ax.plot(x_vals, y_dipertimbangkan, label="Dipertimbangkan", color="#ffa500", linewidth=2.5)
    ax.plot(x_vals, y_layak, label="Layak", color="#21c354", linewidth=2.5)
    
    ax.axvline(x=x_input, color="#3b82f6", linestyle="--", linewidth=2, label=f"Input IPK: {x_input}")
    
    ax.plot(x_input, val_tidak_layak, 'o', color="#ff4b4b", markersize=8)
    ax.plot(x_input, val_dipertimbangkan, 'o', color="#ffa500", markersize=8)
    ax.plot(x_input, val_layak, 'o', color="#21c354", markersize=8)
    
    ax.set_title("Kurva Himpunan Fuzzy Kelayakan Beasiswa", fontsize=14, fontweight='bold')
    ax.set_xlabel("Nilai IPK", fontsize=12)
    ax.set_ylabel("Derajat Keanggotaan (μ)", fontsize=12)
    ax.set_xlim(0, 4.0)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    ax.grid(True, linestyle="--", alpha=0.5)
    
    st.pyplot(fig)

with tab4:
    st.header("Interpretasi Hasil (Defuzzifikasi)")
    st.write("Menggunakan Metode **Centroid** untuk mendapatkan *Crisp Output*.")
    
    c_tidak_layak = 20
    c_dipertimbangkan = 50
    c_layak = 80
    
    total_bobot = val_tidak_layak + val_dipertimbangkan + val_layak
    
    if total_bobot > 0:
        z = ((val_tidak_layak * c_tidak_layak) + (val_dipertimbangkan * c_dipertimbangkan) + (val_layak * c_layak)) / total_bobot
    else:
        z = 0

    st.latex(rf"Z = \frac{{({val_tidak_layak:.2f} \times {c_tidak_layak}) + ({val_dipertimbangkan:.2f} \times {c_dipertimbangkan}) + ({val_layak:.2f} \times {c_layak})}}{{{total_bobot:.2f}}} = {z:.2f}")

    if z <= 40:
        kesimpulan = "Tidak Layak"
    elif 40 < z <= 70:
        kesimpulan = "Dipertimbangkan"
    else:
        kesimpulan = "Layak"

    st.info(f"**Nilai Crisp Output (Skala 0-100):** {z:.2f}")
    st.success(f" **Keputusan Akhir:** Mahasiswa dinyatakan **{kesimpulan}** untuk menerima beasiswa.")
