import streamlit as st

st.set_page_config(page_title="Calculatrice MDB", page_icon="🏢", layout="centered")

# ==============================================================================
# CSS & STYLE (COPIE EXACTE DE LA VERSION FLASH VALIDÉE)
# ==============================================================================
st.markdown("""
<style>
    /* 1. STICKY FOOTER */
    .fixed-footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #ffffff; border-top: 1px solid #e0e0e0;
        text-align: center; padding: 12px 0; z-index: 99999;
        box-shadow: 0px -4px 15px rgba(0,0,0,0.08); font-family: sans-serif;
    }
    .footer-label { font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; }
    .footer-value { font-size: 1.6rem; font-weight: 800; }
    
    /* 2. FORCER LES COLONNES SUR MOBILE */
    [data-testid="column"] {
        width: 50% !important; flex: 0 0 50% !important; min-width: 50% !important; padding: 0 4px !important;
    }
    
    /* 3. DESIGN "BLUE BOX" (Résultats) */
    .result-box {
        background-color: #f0f7ff; border: 1px solid #cce5ff; border-radius: 8px;
        padding: 10px 5px; text-align: center; height: 74px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin-top: 2px;
    }
    .result-label { font-size: 0.7rem; color: #555; text-transform: uppercase; margin-bottom: 2px;}
    .result-value { font-size: 1.1rem; font-weight: 800; color: #0068c9; }

    /* 4. BOUTONS RADIOS */
    div.row-widget.stRadio > div {flex-direction: row; justify-content: center; gap: 5px;}
    div.row-widget.stRadio > div > label {
        background-color: transparent; border: 1px solid #ddd; padding: 8px 5px;
        border-radius: 6px; font-size: 0.8rem; cursor: pointer; width: 100%; text-align: center;
    }
    div.row-widget.stRadio > div > label[data-baseweb="radio"] {
        background-color: #2e2e2e; color: white; border-color: #2e2e2e;
    }

    /* 5. SYNTHÈSE KPI */
    .kpi-container {
        display: flex; flex-direction: row; justify-content: space-between;
        background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; margin-top: 10px;
    }
    .kpi-box { width: 48%; text-align: center; }
    .kpi-label { font-size: 0.8rem; color: #666; margin-bottom: 5px; }
    .kpi-value { font-size: 1.2rem; font-weight: 700; color: #000; }
    
    .block-container { padding-top: 1rem; padding-bottom: 6rem; }
</style>
""", unsafe_allow_html=True)

# --- FONCTIONS CUSTOM ---
def display_blue_result(label, value):
    st.markdown(f"""<div class="result-box"><div class="result-label">{label}</div><div class="result-value">{value}</div></div>""", unsafe_allow_html=True)

def display_custom_kpi(label1, value1, label2, value2):
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-box"><div class="kpi-label">{label1}</div><div class="kpi-value">{value1}</div></div>
        <div style="border-left: 1px solid #ddd; height: 40px; margin: auto 0;"></div>
        <div class="kpi-box"><div class="kpi-label">{label2}</div><div class="kpi-value">{value2}</div></div>
    </div>""", unsafe_allow_html=True)

st.title("🏢 Calculatrice MDB")

tab_flash, tab_expert = st.tabs(["⚡ FLASH", "🏢 EXPERT"])

# ==============================================================================
# ONGLET 1 : FLASH (VALIDÉ V30)
# ==============================================================================
with tab_flash:
    with st.expander("1️⃣ ACQUISITION", expanded=True):
        c1, c2 = st.columns(2)
        surf_flash = c1.number_input("Surface (m²)", value=20.0, step=1.0, key="f_surf")
        prix_flash = c2.number_input("Prix Net (€)", value=200000, step=1000, key="f_prix")
        if surf_flash > 0:
            display_blue_result("PRIX ACTUEL", f"{prix_flash/surf_flash:,.0f} €/m²")

    with st.expander("2️⃣ TRAVAUX", expanded=False):
        mode_travaux_flash = st.radio("Mode :", ["€/m²", "Montant"], horizontal=True, label_visibility="collapsed", key="f_mode_travaux")
        c3, c4 = st.columns(2)
        if mode_travaux_flash == "€/m²":
            cout_m2_flash = c3.number_input("Coût/m²", value=2000, step=100, key="f_cout_m2")
            total_travaux_flash = surf_flash * cout_m2_flash
            with c4: display_blue_result("BUDGET TOTAL", f"{total_travaux_flash/1000:.1f} k€")
        else:
            total_travaux_flash = c3.number_input("Total (€)", value=40000, step=1000, key="f_total_travaux")
            with c4:
                val_m2 = f"{total_travaux_flash/surf_flash:,.0f} €" if surf_flash > 0 else "0 €"
                display_blue_result("SOIT AU M²", val_m2)

    with st.expander("3️⃣ REVENTE", expanded=False):
        mode_revente_flash = st.radio("Mode :", ["€/m²", "Montant"], horizontal=True, label_visibility="collapsed", key="f_mode_revente")
        c5, c6 = st.columns(2)
        if mode_revente_flash == "€/m²":
            prix_revente_m2_flash = c5.number_input("Vente/m²", value=12000, step=100, key="f_revente_m2")
            prix_revente_total_flash = surf_flash * prix_revente_m2_flash
            with c6: display_blue_result("PRIX DE SORTIE", f"{prix_revente_total_flash/1000:.0f} k€")
        else:
            prix_revente_total_flash = c5.number_input("Prix de sortie", value=340000, step=5000, key="f_revente_global")
            with c6:
                val_m2 = f"{prix_revente_total_flash/surf_flash:,.0f} €" if surf_flash > 0 else "0 €"
                display_blue_result("SOIT AU M²", val_m2)

    include_notaire = st.checkbox("Inclure Notaire (3%)", value=False, key="f_check_notaire")
    frais_notaire_flash = prix_flash * 0.03 if include_notaire else 0
    cout_total_flash = prix_flash + total_travaux_flash + frais_notaire_flash
    marge_flash = prix_revente_total_flash - cout_total_flash
    renta_flash = (marge_flash / cout_total_flash * 100) if cout_total_flash > 0 else 0

    st.markdown("### 📊 Synthèse")
    display_custom_kpi("COÛT DE L'OPÉRATION", f"{cout_total_flash/1000:.0f} k€", "MARGE", f"{marge_flash/1000:.0f} k€")
    st.markdown('<div class="safe-zone"></div>', unsafe_allow_html=True)

    color_renta = "#d32f2f" # Rouge
    if renta_flash >= 25: color_renta = "#f57c00" # Orange
    if renta_flash >= 40: color_renta = "#388e3c" # Vert
    
    html_footer = f"""<div class="fixed-footer"><div class="footer-label">RENTABILITÉ</div><div class="footer-value" style="color: {color_renta};">{renta_flash:.1f} %</div></div>"""
    st.markdown(html_footer, unsafe_allow_html=True)


# ==============================================================================
# ONGLET 2 : EXPERT (DESIGN UNIFIÉ AVEC FLASH)
# ==============================================================================
with tab_expert:
    # Init variables pour calculs intermédiaires
    total_travaux_expert = 0
    enveloppe_physique = 0
    frais_notaire_expert = 0
    
    # 1. ACQUISITION
    with st.expander("1️⃣ ACQUISITION", expanded=True):
        c1, c2 = st.columns(2)
        surface = c1.number_input("Surface (m²)", value=46.6, step=0.1, key="e_surf")
        prix_offre = c2.number_input("Prix Net (€)", value=240000, step=1000, key="e_prix")
        
        # Ligne 2 : Prix m2 (Bleu)
        if surface > 0:
            display_blue_result("PRIX ACTUEL", f"{prix_offre/surface:,.0f} €/m²")
        
        st.markdown("---")
        
        # Ligne 3 : Agence & Notaire
        c3, c4 = st.columns(2)
        with c3:
            st.write("Frais Agence")
            mode_agence = st.radio("Type", ["%", "Fixe (€)"], horizontal=True, label_visibility="collapsed", key="e_mode_agence")
            if mode_agence == "%":
                taux_agence = st.number_input("Taux (%)", value=0.0, step=0.5, key="e_taux_agence")
                frais_agence_acq = prix_offre * (taux_agence / 100)
            else:
                frais_agence_acq = st.number_input("Montant (€)", value=0, step=500, key="e_montant_agence")
        
        frais_notaire_expert = prix_offre * 0.03
        with c4:
            st.write("Notaire") # Espace pour aligner
            display_blue_result("NOTAIRE (3%)", f"{frais_notaire_expert:,.0f} €")

    # 2. TRAVAUX
    with st.expander("2️⃣
