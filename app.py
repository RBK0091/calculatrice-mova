import streamlit as st

st.set_page_config(page_title="Calculatrice MDB", page_icon="🏢", layout="centered")

# ==============================================================================
# CSS AGRESSIF (FORCE L'AFFICHAGE CÔTE À CÔTE SUR MOBILE)
# ==============================================================================
st.markdown("""
<style>
    /* 1. STICKY FOOTER (Barre Rentabilité) */
    .fixed-footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #ffffff; border-top: 1px solid #e0e0e0;
        text-align: center; padding: 12px 0; z-index: 99999;
        box-shadow: 0px -4px 15px rgba(0,0,0,0.08); font-family: sans-serif;
    }
    .footer-label { font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; }
    .footer-value { font-size: 1.6rem; font-weight: 800; }
    
    /* 2. FORCER LES COLONNES CÔTE À CÔTE SUR MOBILE (OVERRIDE STREAMLIT) */
    [data-testid="column"] {
        width: 50% !important;
        flex: 0 0 50% !important;
        min-width: 50% !important;
        padding: 0 5px !important; /* Réduire les marges pour que ça rentre */
    }
    
    /* 3. DESIGN DES BOUTONS RADIOS */
    div.row-widget.stRadio > div {flex-direction: row; justify-content: center; gap: 5px;}
    div.row-widget.stRadio > div > label {
        background-color: transparent; border: 1px solid #ddd; padding: 8px 5px;
        border-radius: 6px; font-size: 0.8rem; cursor: pointer; width: 100%; text-align: center;
    }
    div.row-widget.stRadio > div > label[data-baseweb="radio"] {
        background-color: #2e2e2e; color: white; border-color: #2e2e2e;
    }

    /* 4. DESIGN CUSTOM POUR LA SYNTHÈSE (HTML) */
    .kpi-container {
        display: flex; flex-direction: row; justify-content: space-between;
        background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee;
        margin-top: 10px;
    }
    .kpi-box { width: 48%; text-align: center; }
    .kpi-label { font-size: 0.8rem; color: #666; margin-bottom: 5px; }
    .kpi-value { font-size: 1.2rem; font-weight: 700; color: #000; }
    
    /* Ajustements généraux */
    .block-container { padding-top: 1rem; padding-bottom: 6rem; }
    .stNumberInput label { font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# --- FONCTION POUR AFFICHER LES RÉSULTATS GARANTIS CÔTE À CÔTE ---
def display_custom_kpi(label1, value1, label2, value2):
    html = f"""
    <div class="kpi-container">
        <div class="kpi-box">
            <div class="kpi-label">{label1}</div>
            <div class="kpi-value">{value1}</div>
        </div>
        <div style="border-left: 1px solid #ddd; height: 40px; margin: auto 0;"></div>
        <div class="kpi-box">
            <div class="kpi-label">{label2}</div>
            <div class="kpi-value">{value2}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

st.title("🏢 Calculatrice MDB")

# Création des onglets
tab_flash, tab_expert = st.tabs(["⚡ FLASH", "🏢 EXPERT"])

# ==============================================================================
# ONGLET 1 : FLASH (DESIGN MOBILE FORCÉ)
# ==============================================================================
with tab_flash:
    
    # --- 1. ACQUISITION ---
    with st.expander("1️⃣ ACQUISITION", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            surf_flash = st.number_input("Surface (m²)", value=20.0, step=1.0, key="f_surf")
        with c2:
            prix_flash = st.number_input("Prix (€)", value=200000, step=1000, key="f_prix")
        
        # Résultat visuel immédiat (HTML custom pour être sûr)
        if surf_flash > 0:
            st.markdown(f"<div style='text-align:center; font-weight:bold; color:#0068c9; margin-top:5px; font-size:0.9rem;'>📍 {prix_flash/surf_flash:,.0f} €/m²</div>", unsafe_allow_html=True)

    # --- 2. TRAVAUX ---
    with st.expander("2️⃣ TRAVAUX", expanded=False):
        mode_travaux_flash = st.radio("Mode :", ["€/m²", "Global"], horizontal=True, label_visibility="collapsed", key="f_mode_travaux")
        
        c3, c4 = st.columns(2)
        if mode_travaux_flash == "€/m²":
            with c3:
                cout_m2_flash = st.number_input("Coût/m²", value=2000, step=100, key="f_cout_m2")
                total_travaux_flash = surf_flash * cout_m2_flash
            with c4:
                # On utilise un input désactivé pour afficher le résultat "comme" un input, aligné
                st.text_input("Budget", value=f"{total_travaux_flash/1000:.1f} k€", disabled=True, key="res_tx_1")
        else:
            with c3:
                total_travaux_flash = st.number_input("Total (€)", value=40000, step=1000, key="f_total_travaux")
            with c4:
                 if surf_flash > 0:
                    st.text_input("Soit/m²", value=f"{total_travaux_flash/surf_flash:,.0f} €", disabled=True, key="res_tx_2")
                 else:
                    st.text_input("Soit/m²", value="0 €", disabled=True)

    # --- 3. REVENTE ---
    with st.expander("3️⃣ REVENTE", expanded=False):
        mode_revente_flash = st.radio("Mode :", ["€/m²", "Global"], horizontal=True, label_visibility="collapsed", key="f_mode_revente")
        
        c5, c6 = st.columns(2)
        if mode_revente_flash == "€/m²":
            with c5:
                prix_revente_m2_flash = st.number_input("Vente/m²", value=12000, step=100, key="f_revente_m2")
                prix_revente_total_flash = surf_flash * prix_revente_m2_flash
            with c6:
                st.text_input("C.A.", value=f"{prix_revente_total_flash/1000:.0f} k€", disabled=True, key="res_rev_1")
        else:
            with c5:
                prix_revente_total_flash = st.number_input("Prix Global", value=340000, step=5000, key="f_revente_global")
            with c6:
                if surf_flash > 0:
                    st.text_input("Soit/m²", value=f"{prix_revente_total_flash/surf_flash:,.0f} €", disabled=True, key="res_rev_2")
                else:
                    st.text_input("Soit/m²", value="0 €", disabled=True)

    # --- CALCULS ---
    include_notaire = st.checkbox("Inclure Notaire (3%)", value=False, key="f_check_notaire")
    cout_total_flash = prix_flash + total_travaux_flash
    if include_notaire:
        cout_total_flash += (prix_flash * 0.03)

    marge_flash = prix_revente_total_flash - cout_total_flash
    
    if cout_total_flash > 0:
        renta_flash = (marge_flash / cout_total_flash) * 100
    else:
        renta_flash = 0

    # --- SYNTHÈSE (FORCÉE EN HTML/CSS) ---
    st.markdown("### 📊 Synthèse")
    
    # C'est ici que je force l'affichage côte à côte avec ma fonction personnalisée
    display_custom_kpi(
        "COÛT TOTAL", f"{cout_total_flash/1000:.0f} k€",
        "MARGE BRUTE", f"{marge_flash/1000:.0f} k€"
    )

    # Espace vide pour le scroll
    st.markdown('<div class="safe-zone"></div>', unsafe_allow_html=True)

    # --- STICKY FOOTER ---
    color_renta = "#d32f2f" # Rouge
    if renta_flash >= 25: color_renta = "#f57c00" # Orange
    if renta_flash >= 40: color_renta = "#388e3c" # Vert

    html_footer = f"""
    <div class="fixed-footer">
        <div class="footer-label">RENTABILITÉ BRUTE</div>
        <div class="footer-value" style="color: {color_renta};">
            {renta_flash:.1f} %
        </div>
    </div>
    """
    st.markdown(html_footer, unsafe_allow_html=True)


# ==============================================================================
# ONGLET 2 : EXPERT (CODE SÉCURISÉ)
# ==============================================================================
with tab_expert:
    # Initialisation de toutes les variables pour éviter le "NameError"
    # Cela garantit que le calcul final ne plante jamais
    surface = 0.0
    prix_offre = 0.0
    prix_revente_total = 0.0
    
    st.caption("✅ Moteur Expert (Détail Complet)")

    # 1. ACQUISITION
    with st.container():
        st.subheader("1. Acquisition")
        ec1, ec2 = st.columns(2)
        with ec1:
            surface = st.number_input("Surface (m²)", value=46.6, step=0.1, key="e_surf")
            prix_offre = st.number_input("Prix d'achat (€)", value=240000, step=1000, key="e_prix")
            if surface > 0:
                st.caption(f"📍 {prix_offre/surface:,.0f} €/m²")
        
        with ec2:
            st.write("Frais Agence")
            mode_agence = st.radio("Mode", ["%", "Fixe (€)"], horizontal=True, label_visibility="collapsed", key="e_mode_agence")
            
            if mode_agence == "%":
                taux_agence = st.number_input("Taux (%)", value=0.0, step=0.5, key="e_taux_agence")
                frais_agence_acq = prix_offre * (taux_agence / 100)
            else:
                frais_agence_acq = st.number_input("Montant (€)", value=0, step=500, key="e_montant_agence")
            
            frais_notaire = prix_offre * 0.03
            st.metric("Notaire (3%)", f"{frais_notaire:,.0f} €")

    st.markdown("---")

    # 2. TRAVAUX
    with st.container():
        st.subheader("2. Travaux & Études")
        type_reno = st.selectbox("Gamme Rénovation", 
                             ["Rafraichissement", "Rénovation Simple", "Lourde", "Luxe"], key="e_type_reno")
        
        tc1, tc2 = st.columns(2)
        with tc1:
            cout_travaux_m2 = st.number_input("Coût Tx (€/m²)", value=1500, step=50, key="e_cout_tx")
        with tc2:
            architecte = st.number_input("Architecte (€)", value=0, key="e_archi")

        st.caption("Frais Annexes")
        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            geometre = st.number_input("Géomètre", value=1000, key="e_geo")
        with pc2:
            ingenieur = st.number_input("Ingénieur", value=1000, key="e_inge")
        with pc3:
            age_frais = st.number_input("Frais AGE", value=2000, key="e_age")
        
        autres_frais_travaux = st.number_input("Autres", value=0, key="e_autres")

    st.markdown("---")

    # 3. TEMPS & CHARGES
    with st.container():
        st.subheader("3. Temps & Charges")
        sc1, sc2 = st.columns(2)
        with sc1:
            duree_mois = st.slider("Durée (mois)", 3, 18, 10, key="e_duree")
            retard_mois = st.slider("Retard", 0, 12, 0, key="e_retard")
        with sc2:
            charges_annuelles = st.number_input("Charges/An", value=1200, key="e_charges")
            taxe_fonciere = st.number_input("Taxe Fonc./An", value=917, key="e_tf")

    st.markdown("---")

    # 4. REVENTE
    with st.container():
        st.subheader("4. Revente")
        rc1, rc2 = st.columns(2)
        
        with rc1:
            mode_revente_expert = st.radio("Mode", ["€/m²", "Global €"], horizontal=True, label_visibility="collapsed", key="e_mode_revente")
            if mode_revente_expert == "€/m²":
                prix_revente_m2_expert = st.number_input("Prix/m² (€)", value=10500, step=100, key="e_rev_m2_input")
                prix_revente_total = surface * prix_revente_m2_expert
            else:
                prix_revente_total = st.number_input("Prix Global (€)", value=520000, step=1000, key="e_rev_global_input")
        
        with rc2:
            montant_agence_revente = st.number_input("Frais Agence", value=10000, step=500, key="e_frais_rev")
            st.metric("Total Revente", f"{prix_revente_total:,.0f} €")

    # --- CALCULS FINAUX SÉCURISÉS ---
    budget_travaux_base = surface * cout_travaux_m2
    honoraires_conducteur = budget_travaux_base * 0.05 
    total_travaux = budget_travaux_base + honoraires_conducteur + architecte + geometre + ingenieur + age_frais + autres_frais_travaux
    enveloppe_physique = prix_offre + frais_agence_acq + frais_notaire + total_travaux

    frais_hypotheque = prix_offre * 0.015
    frais_levee = 1500
    duree_totale = duree_mois + retard_mois
    base_portage = enveloppe_physique * 0.75
    interets_portage = base_portage * 0.07 * (duree_totale / 12)
    frais_dossier_banque = 1500 
    total_cout_portage_banque = interets_portage + frais_dossier_banque
    frais_sep = enveloppe_physique * 0.02
    cout_charges_totales = (charges_annuelles * (duree_totale / 12)) + (taxe_fonciere * (duree_totale / 12))

    total_cout_operation = enveloppe_physique + frais_hypotheque + frais_levee + total_cout_portage_banque + frais_sep + cout_charges_totales
    
    net_vendeur_reel = prix_revente_total - montant_agence_revente
    total_plus_value = net_vendeur_reel - total_cout_operation
    
    if total_cout_operation > 0:
        pourcentage_marge = (total_plus_value / total_cout_operation) * 100
    else:
        pourcentage_marge = 0

    # --- RÉSULTATS VISUELS EXPERT ---
    st.markdown("---")
    st.header("📊 Résultats")
    
    # Ici aussi, on utilise la fonction custom pour assurer l'affichage mobile
    display_custom_kpi(
        "PRIX REVENTE", f"{prix_revente_total:,.0f} €",
        "COÛT TOTAL", f"{total_cout_operation:,.0f} €"
    )
    st.metric("PLUS-VALUE NETTE", f"{total_plus_value:,.0f} €")

    st.markdown(f"### 🎯 Rentabilité : {pourcentage_marge:.2f} %")
    if pourcentage_marge < 25:
        st.progress(min(pourcentage_marge/50, 1.0))
        st.error("Trop faible (<25%)")
    elif pourcentage_marge < 40:
        st.progress(min(pourcentage_marge/50, 1.0))
        st.warning("Bon (Partenaire)")
    else:
        st.progress(min(pourcentage_marge/50, 1.0))
        st.success("Excellent (Club MOVA)")

    # --- RÉCAPITULATIF ---
    st.markdown("---")
    with st.expander("🔎 DÉTAIL COMPLET"):
        st.write("### 1. Acquisition & Travaux")
        st.write(f"- Enveloppe Physique : **{enveloppe_physique:,.0f} €**")
        st.caption(f"Dont Notaire : {frais_notaire:,.0f} € | Dont Travaux (+5% cond.) : {total_travaux:,.0f} €")
        
        st.write("### 2. Banque & Garanties")
        st.write(f"- Portage (7%) + Dossier (1500€) : **{total_cout_portage_banque:,.0f} €**")
        st.write(f"- Hypothèque (1,5%) + Levée (1500€) : **{frais_hypotheque + frais_levee:,.0f} €**")
        
        st.write("### 3. Structure & Vie")
        st.write(f"- Frais SEP (2%) : **{frais_sep:,.0f} €**")
        st.write(f"- Charges & TF : **{cout_charges_totales:,.0f} €**")
