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
    with st.expander("2️⃣ TRAVAUX & ÉTUDES", expanded=False):
        type_reno = st.selectbox("Gamme", ["Rafraichissement", "Rénovation Simple", "Lourde", "Luxe"], key="e_type_reno")
        
        c5, c6 = st.columns(2)
        cout_travaux_m2 = c5.number_input("Coût Tx (€/m²)", value=1500, step=50, key="e_cout_tx")
        
        # Calcul Budget Travaux Base
        budget_travaux_base = surface * cout_travaux_m2
        
        # Annexes
        st.caption("Frais Annexes")
        ac1, ac2 = st.columns(2) # 2 colonnes sur mobile c'est mieux
        archi = ac1.number_input("Architecte", value=0, key="e_archi")
        geo = ac2.number_input("Géomètre", value=1000, key="e_geo")
        inge = ac1.number_input("Ingénieur", value=1000, key="e_inge")
        age_frais = ac2.number_input("Frais AGE", value=2000, key="e_age")
        autres = st.number_input("Autres", value=0, key="e_autres")
        
        # Calcul Total Travaux
        honoraires_cond = budget_travaux_base * 0.05
        total_travaux_expert = budget_travaux_base + honoraires_cond + archi + geo + inge + age_frais + autres
        
        st.markdown("---")
        # Affichage du Total Travaux en Bleu
        display_blue_result("ENVELOPPE TRAVAUX", f"{total_travaux_expert:,.0f} €")

    # 3. TEMPS
    with st.expander("3️⃣ TEMPS & CHARGES", expanded=False):
        tc1, tc2 = st.columns(2)
        duree_mois = tc1.slider("Durée (mois)", 3, 18, 10, key="e_duree")
        retard_mois = tc2.slider("Retard", 0, 12, 0, key="e_retard")
        
        tc3, tc4 = st.columns(2)
        charges_an = tc3.number_input("Charges/An", value=1200, key="e_charges")
        tf_an = tc4.number_input("Taxe Fonc./An", value=917, key="e_tf")
        
        # Calculs Intermédiaires pour le "Bleu"
        enveloppe_physique = prix_offre + frais_agence_acq + frais_notaire_expert + total_travaux_expert
        duree_totale = duree_mois + retard_mois
        # Frais Financiers
        base_portage = enveloppe_physique * 0.75
        interets = base_portage * 0.07 * (duree_totale / 12)
        frais_dossier = 1500
        # Charges
        charges_prorata = (charges_an + tf_an) * (duree_totale / 12)
        
        cout_temps_total = interets + frais_dossier + charges_prorata
        
        st.markdown("---")
        display_blue_result("COÛT DU TEMPS (FIN + CHG)", f"{cout_temps_total:,.0f} €")

    # 4. REVENTE
    with st.expander("4️⃣ REVENTE", expanded=False):
        mode_revente_expert = st.radio("Mode", ["€/m²", "Montant"], horizontal=True, label_visibility="collapsed", key="e_mode_revente")
        
        rc1, rc2 = st.columns(2)
        prix_revente_total_expert = 0
        
        if mode_revente_expert == "€/m²":
            prix_rev_m2 = rc1.number_input("Vente/m²", value=10500, step=100, key="e_rev_m2_ex")
            prix_revente_total_expert = surface * prix_rev_m2
            with rc2: display_blue_result("PRIX DE SORTIE", f"{prix_revente_total_expert/1000:.0f} k€")
        else:
            prix_revente_total_expert = rc1.number_input("Prix de sortie", value=520000, step=5000, key="e_rev_glob_ex")
            with rc2:
                val_m2 = f"{prix_revente_total_expert/surface:,.0f} €" if surface > 0 else "0 €"
                display_blue_result("SOIT AU M²", val_m2)
        
        st.markdown("---")
        frais_agence_rev = st.number_input("Frais Agence Revente (€)", value=10000, step=500, key="e_frais_rev")

    # --- CALCULS FINAUX EXPERT ---
    frais_hypotheque = prix_offre * 0.015
    frais_levee = 1500
    frais_sep = enveloppe_physique * 0.02
    
    total_cout_op_expert = enveloppe_physique + frais_hypotheque + frais_levee + cout_temps_total + frais_sep
    net_vendeur_reel = prix_revente_total_expert - frais_agence_rev
    marge_nette_expert = net_vendeur_reel - total_cout_op_expert
    
    renta_expert = (marge_nette_expert / total_cout_op_expert * 100) if total_cout_op_expert > 0 else 0

    # --- SYNTHÈSE EXPERT ---
    st.markdown("### 📊 Synthèse")
    display_custom_kpi("COÛT DE L'OPÉRATION", f"{total_cout_op_expert/1000:.0f} k€", "MARGE", f"{marge_nette_expert/1000:.0f} k€")
    
    st.markdown('<div class="safe-zone"></div>', unsafe_allow_html=True)

    # Note : Le sticky footer est global, il affiche la renta calculée dans l'onglet actif.
    # Mais Streamlit exécute tout le script. 
    # ASTUCE : On ré-affiche le footer ICI pour écraser celui du Flash si on est dans l'onglet Expert.
    
    color_renta_ex = "#d32f2f"
    if renta_expert >= 25: color_renta_ex = "#f57c00"
    if renta_expert >= 40: color_renta_ex = "#388e3c"

    html_footer_ex = f"""<div class="fixed-footer"><div class="footer-label">RENTABILITÉ</div><div class="footer-value" style="color: {color_renta_ex};">{renta_expert:.1f} %</div></div>"""
    st.markdown(html_footer_ex, unsafe_allow_html=True)

    # --- RÉCAPITULATIF ---
    with st.expander("🔎 DÉTAIL COMPLET"):
        st.write("### 1. Acquisition & Travaux")
        st.write(f"- Enveloppe Physique : **{enveloppe_physique:,.0f} €**")
        
        st.write("### 2. Banque & Garanties")
        st.write(f"- Coût du Temps (Intérêts + Charges) : **{cout_temps_total:,.0f} €**")
        st.write(f"- Hypothèque + Levée : **{frais_hypotheque + frais_levee:,.0f} €**")
        
        st.write("### 3. Structure")
        st.write(f"- Frais SEP (2%) : **{frais_sep:,.0f} €**")
