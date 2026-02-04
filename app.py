import streamlit as st

st.set_page_config(page_title="Calculatrice MDB - MOVA", page_icon="🏢", layout="centered")

# CSS pour un affichage propre sur mobile
st.markdown("""
<style>
div.row-widget.stRadio > div {flex-direction: row; justify-content: center;}
div.row-widget.stRadio > div > label {
    background-color: #f0f2f6; padding: 5px 15px; border-radius: 8px; margin: 0 5px; cursor: pointer; border: 1px solid #d1d5db;
}
div.row-widget.stRadio > div > label[data-baseweb="radio"] {background-color: #ff4b4b; color: white;}
.streamlit-expanderHeader {font-weight: bold; font-size: 1.1rem;}
</style>
""", unsafe_allow_html=True)

st.title("🏢 Calculatrice MDB (V21)")

# Création des onglets
tab_flash, tab_expert = st.tabs(["⚡ FLASH (Pilotage)", "🏢 EXPERT (Détaillé)"])

# ==============================================================================
# ONGLET 1 : CALCUL FLASH (SIMPLE & VISUEL)
# ==============================================================================
with tab_flash:
    st.info("🎯 Glisse les réglettes : la Rentabilité s'ajuste en temps réel.")

    # 1. LA BASE (Surface)
    # On garde un input simple ici car ça ne change pas toutes les 2 secondes
    surf_flash = st.number_input("📏 Surface (m²)", value=46.0, step=1.0)

    st.markdown("---")

    # 2. LES LEVIERS (Sliders uniquement pour fluidité maximale)
    
    # A. PRIX ACHAT
    st.write("💶 **Prix d'Achat (€)**")
    # Une seule réglette large pour "sentir" le prix
    prix_flash = st.slider("Achat", 0, 1000000, 240000, 5000, label_visibility="collapsed")
    if surf_flash > 0:
        st.caption(f"Soit **{prix_flash/surf_flash:,.0f} €/m²**")

    # B. TRAVAUX
    st.write("🛠️ **Coût Travaux (€/m²)**")
    cout_m2_flash = st.slider("Travaux", 0, 3000, 1500, 50, label_visibility="collapsed")
    total_travaux_flash = surf_flash * cout_m2_flash
    st.caption(f"Budget Travaux : **{total_travaux_flash:,.0f} €**")

    # C. REVENTE
    st.write("💰 **Revente Estimée (€/m²)**")
    prix_revente_m2_flash = st.slider("Revente", 1000, 20000, 10500, 100, label_visibility="collapsed")
    prix_revente_total_flash = surf_flash * prix_revente_m2_flash
    st.caption(f"Total Revente : **{prix_revente_total_flash:,.0f} €**")

    # --- CALCULS ---
    # Option Notaire
    include_notaire = st.checkbox("Inclure Notaire (3%)", value=False)
    
    # Coûts
    frais_notaire_flash = prix_flash * 0.03 if include_notaire else 0
    cout_total_flash = prix_flash + total_travaux_flash + frais_notaire_flash
    
    # Marge
    marge_flash = prix_revente_total_flash - cout_total_flash
    
    # Rentabilité
    if cout_total_flash > 0:
        renta_flash = (marge_flash / cout_total_flash) * 100
    else:
        renta_flash = 0

    # --- RÉSULTATS & CIBLE ---
    st.markdown("---")
    
    # Affichage compact
    c1, c2 = st.columns(2)
    c1.metric("Coût Total", f"{cout_total_flash:,.0f} €")
    
    # Couleur dynamique Renta
    if renta_flash < 25:
        c2.metric("Rentabilité", f"{renta_flash:.1f} %", delta="- Faible", delta_color="inverse")
    elif renta_flash < 40:
        c2.metric("Rentabilité", f"{renta_flash:.1f} %", delta="Standard", delta_color="off")
    else:
        c2.metric("Rentabilité", f"{renta_flash:.1f} %", delta="EXCELLENT", delta_color="normal")

    # --- L'ARME FATALE : CALCUL DU PRIX CIBLE POUR 40% ---
    st.markdown("---")
    st.subheader("🎯 Objectif Club MOVA (40%)")
    
    # Formule inversée : (Revente - Coûts) / Coûts = 0.40
    # Revente = 1.40 * Coûts
    # Coûts_Cible = Revente / 1.40
    # Prix_Achat_Cible = Coûts_Cible - Travaux (- Notaire éventuel)
    
    cout_cible_pour_40 = prix_revente_total_flash / 1.40
    if include_notaire:
        # Si notaire inclus : Prix_Cible + 0.03*Prix_Cible = Enveloppe_Dispo - Travaux
        # 1.03 * Prix_Cible = Enveloppe_Dispo - Travaux
        enveloppe_dispo = cout_cible_pour_40 - total_travaux_flash
        prix_achat_cible = enveloppe_dispo / 1.03
    else:
        prix_achat_cible = cout_cible_pour_40 - total_travaux_flash

    if prix_achat_cible > 0:
        st.success(f"Pour atteindre **40%**, ton offre max doit être de : **{prix_achat_cible:,.0f} €**")
    else:
        st.error("Impossible d'atteindre 40% avec ces travaux/revente (Prix négatif).")


# ==============================================================================
# ONGLET 2 : CALCUL EXPERT (LE MOTEUR V17 FIABLE)
# ==============================================================================
with tab_expert:
    st.caption("✅ Moteur Expert V17 (Détail Complet)")

    # 1. ACQUISITION
    with st.container():
        st.subheader("1. Acquisition")
        ec1, ec2 = st.columns(2)
        with ec1:
            surface = st.number_input("Surface (m²)", value=46.6, step=0.1, min_value=0.0, max_value=2000.0, key="e_surf")
            prix_offre = st.number_input("Prix d'achat (€)", value=240000, step=1000, min_value=0, max_value=5000000, key="e_prix")
            if surface > 0:
                st.caption(f"📍 {prix_offre/surface:,.0f} €/m²")
        
        with ec2:
            st.write("Frais d'agence (Achat)")
            mode_agence = st.radio("Saisie Agence", ["%", "Fixe (€)"], horizontal=True, label_visibility="collapsed", key="e_mode_agence")
            
            if mode_agence == "%":
                taux_agence = st.number_input("Taux (%)", value=0.0, step=0.5, key="e_taux_agence")
                frais_agence_acq = prix_offre * (taux_agence / 100)
            else:
                frais_agence_acq = st.number_input("Montant (€)", value=0, step=500, key="e_montant_agence")
            
            frais_notaire = prix_offre * 0.03
            st.info(f"👮‍♂️ Notaire (3%): **{frais_notaire:,.0f} €**")

    st.markdown("---")

    # 2. TRAVAUX & ETUDES
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
        
        autres_frais_travaux = st.number_input("Autres (Permis...)", value=0, key="e_autres")

    st.markdown("---")

    # 3. TEMPS & CHARGES
    with st.container():
        st.subheader("3. Temps & Charges")
        sc1, sc2 = st.columns(2)
        with sc1:
            duree_mois = st.slider("Durée (3-18 mois)", 3, 18, 10, key="e_duree")
            retard_mois = st.slider("Retard Prévu", 0, 12, 0, key="e_retard")
        with sc2:
            charges_annuelles = st.number_input("Charges/An (€)", value=1200, key="e_charges")
            taxe_fonciere = st.number_input("Taxe Fonc./An (€)", value=917, key="e_tf")

    st.markdown("---")

    # 4. REVENTE
    with st.container():
        st.subheader("4. Revente")
        rc1, rc2 = st.columns(2)
        with rc1:
            mode_revente_expert = st.radio("Mode Revente", ["€/m²", "Global €"], horizontal=True, label_visibility="collapsed", key="e_mode_revente")
            if mode_revente_expert == "€/m²":
                prix_revente_m2_expert = st.number_input("Prix/m² (€)", value=10500, step=100, max_value=50000, key="e_rev_m2_input")
                prix_revente_total = surface * prix_revente_m2_expert
            else:
                prix_revente_total = st.number_input("Prix Global (€)", value=520000, step=1000, max_value=10000000, key="e_rev_global_input")
        
        with rc2:
            montant_agence_revente = st.number_input("Frais Agence Vente (€)", value=10000, step=500, key="e_frais_rev")
            if mode_revente_expert == "€/m²":
                st.info(f"Total: **{prix_revente_total:,.0f} €**")
            elif surface > 0:
                st.info(f"Soit: **{prix_revente_total/surface:,.0f} €/m²**")

    # --- MOTEUR DE CALCUL EXPERT (V14) ---
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
    
    res1, res2, res3 = st.columns(3)
    res1.metric("Prix Revente", f"{prix_revente_total:,.0f} €")
    res2.metric("Coût Total", f"{total_cout_operation:,.0f} €")
    res3.metric("Plus-Value Net", f"{total_plus_value:,.0f} €", delta_color="normal")

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

    # --- RÉCAPITULATIF COMPLET ---
    st.markdown("---")
    with st.expander("🔎 DÉTAIL COMPLET (Cliquer pour ouvrir)"):
        st.write("### 1. Acquisition & Travaux")
        st.write(f"- Enveloppe Physique : **{enveloppe_physique:,.0f} €**")
        st.caption(f"Dont Notaire : {frais_notaire:,.0f} € | Dont Travaux (+5% cond.) : {total_travaux:,.0f} €")
        
        st.write("### 2. Banque & Garanties")
        st.write(f"- Portage (7%) + Dossier (1500€) : **{total_cout_portage_banque:,.0f} €**")
        st.write(f"- Hypothèque (1,5%) + Levée (1500€) : **{frais_hypotheque + frais_levee:,.0f} €**")
        
        st.write("### 3. Structure & Vie")
        st.write(f"- Frais SEP (2%) : **{frais_sep:,.0f} €**")
        st.write(f"- Charges & TF : **{cout_charges_totales:,.0f} €**")
