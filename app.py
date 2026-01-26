import streamlit as st

st.set_page_config(page_title="Calculatrice MDB - MOVA", page_icon="🏢")

st.title("🏢 Calculatrice Rentabilité MDB (V11)")
st.success("✅ V11 : Affichage dynamique Prix m² <-> Prix Total (Revente)")
st.markdown("---")

# Création des onglets
tab_flash, tab_expert = st.tabs(["⚡ CALCUL FLASH (Visite)", "🏢 CALCUL EXPERT (Détaillé)"])

# ==============================================================================
# ONGLET 1 : CALCUL FLASH (SIMPLE)
# ==============================================================================
with tab_flash:
    st.header("⚡ Rentabilité Immédiate")
    st.info("Mode simplifié pour prise de décision rapide en visite.")

    # 1. ACQUISITION
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        surf_flash = st.number_input("Surface (m²)", value=20.0, step=1.0, key="f_surf")
        prix_flash = st.number_input("Prix d'achat (€)", value=200000, step=1000, key="f_prix")
    
    with col_f2:
        if surf_flash > 0:
            pm2_flash = prix_flash / surf_flash
            st.metric("Prix Achat au m²", f"{pm2_flash:,.0f} €/m²")
        else:
            st.metric("Prix Achat au m²", "0 €/m²")

    # 2. TRAVAUX
    st.write("---")
    st.write("🛠️ Estimation Travaux")
    mode_travaux_flash = st.radio("Mode de calcul travaux :", ["Par m² (€/m²)", "Forfait Global (€)"], horizontal=True, key="f_mode_travaux")
    
    if mode_travaux_flash == "Par m² (€/m²)":
        cout_m2_flash = st.number_input("Coût Travaux au m² (€)", value=2000, step=100, key="f_cout_m2")
        total_travaux_flash = surf_flash * cout_m2_flash
        st.write(f"👉 Budget travaux : **{total_travaux_flash:,.0f} €**")
    else:
        total_travaux_flash = st.number_input("Montant Total Travaux (€)", value=40000, step=1000, key="f_total_travaux")

    # 3. REVENTE (AMÉLIORATION V11 : APERÇU DIRECT)
    st.write("---")
    st.write("💰 Estimation Revente")
    
    mode_revente_flash = st.radio("Saisie Revente :", ["Par m² (€/m²)", "Prix Global (€)"], horizontal=True, key="f_mode_revente")
    
    if mode_revente_flash == "Par m² (€/m²)":
        prix_revente_m2_flash = st.number_input("Prix Revente Estimé au m² (€)", value=12000, step=100, key="f_revente_m2")
        prix_revente_total_flash = surf_flash * prix_revente_m2_flash
        # Affichage dynamique du total
        st.info(f"Soit un Prix Total de : **{prix_revente_total_flash:,.0f} €**")
    else:
        prix_revente_total_flash = st.number_input("Prix Revente Global Estimé (€)", value=340000, step=5000, key="f_revente_global")
        # Affichage dynamique du m²
        if surf_flash > 0:
            calc_m2_flash = prix_revente_total_flash / surf_flash
            st.info(f"Soit un prix au m² de : **{calc_m2_flash:,.0f} €/m²**")

    # CALCUL DE RENTABILITÉ
    include_notaire = st.checkbox("Inclure Notaire (3%) dans le coût ?", value=False, key="f_check_notaire")
    
    cout_total_flash = prix_flash + total_travaux_flash
    if include_notaire:
        cout_total_flash += (prix_flash * 0.03)

    marge_flash = prix_revente_total_flash - cout_total_flash
    
    if cout_total_flash > 0:
        renta_flash = (marge_flash / cout_total_flash) * 100
    else:
        renta_flash = 0

    # AFFICHAGE RÉSULTATS FLASH
    st.write("---")
    c_res1, c_res2 = st.columns(2)
    c_res1.metric("Coût Total (Achat+Tx)", f"{cout_total_flash:,.0f} €")
    c_res2.metric("Rentabilité Brute", f"{renta_flash:.2f} %")

    if renta_flash < 25:
        st.error(f"🛑 {renta_flash:.1f}% - NE PAS ACHETER (Trop faible)")
    elif renta_flash < 40:
        st.warning(f"⚠️ {renta_flash:.1f}% - PROJET MOYEN (Cible Partenaire)")
    else:
        st.success(f"🚀 {renta_flash:.1f}% - GO ! (Cible Club MOVA)")


# ==============================================================================
# ONGLET 2 : CALCUL EXPERT (COMPLET V11)
# ==============================================================================
with tab_expert:
    st.header("🏢 Analyse Détaillée (Certifiée)")
    st.success("✅ V11 : Moteur complet avec conversions automatiques")

    # --- 1. ACQUISITION ---
    st.subheader("1. Acquisition")
    col1, col2 = st.columns(2)
    with col1:
        surface = st.number_input("Surface (m²)", value=46.6, step=0.1, key="e_surf")
        prix_offre = st.number_input("Prix d'achat (€)", value=240000, step=1000, key="e_prix")
        
        if surface > 0:
            prix_m2_achat = prix_offre / surface
            st.info(f"Prix au m² : {prix_m2_achat:,.0f} €/m²")
        
    with col2:
        st.write("Frais d'agence (Achat)")
        mode_agence = st.radio("Mode de saisie", ["En %", "Montant Fixe (€)"], horizontal=True, label_visibility="collapsed", key="e_mode_agence")
        
        if mode_agence == "En %":
            taux_agence = st.number_input("Taux Agence (%)", value=0.0, step=0.5, key="e_taux_agence")
            frais_agence_acq = prix_offre * (taux_agence / 100)
            if frais_agence_acq > 0:
                st.info(f"Montant : {frais_agence_acq:,.0f} €")
        else:
            frais_agence_acq = st.number_input("Montant Agence (€)", value=0, step=500, key="e_montant_agence")
        
        frais_notaire = prix_offre * 0.03
        st.info(f"Frais Notaire (3% MDB) : {frais_notaire:,.0f} €")

    # --- 2. TRAVAUX & ETUDES ---
    st.subheader("2. Travaux & Études")
    type_reno = st.selectbox("Type de Rénovation", 
                             ["Rafraichissement (400-800€)", "Rénovation Simple (1200-1400€)", "Lourde (1500-1800€)", "Luxe (>2000€)"], key="e_type_reno")

    col3, col4 = st.columns(2)
    with col3:
        cout_travaux_m2 = st.number_input("Coût Travaux (€/m²)", value=1500, step=50, key="e_cout_tx")
        architecte = st.number_input("Architecte et suivi de travaux (€)", value=0, key="e_archi")

    with col4:
        geometre = st.number_input("Géomètre (€)", value=1000, key="e_geo")
        ingenieur = st.number_input("Ingénieur Béton (€)", value=1000, key="e_inge")
        age_frais = st.number_input("Frais AGE / RCP (€)", value=2000, key="e_age")
        autres_frais_travaux = st.number_input("Autres (Permis, etc.) (€)", value=0, key="e_autres")

    # --- 3. PARAMÈTRES TEMPORELS ---
    st.subheader("3. Temps & Charges")
    col5, col6 = st.columns(2)
    with col5:
        duree_mois = st.slider("Durée projet (mois)", 6, 24, 10, key="e_duree")
        retard_mois = st.slider("Marge sécurité retard (mois)", 0, 12, 0, key="e_retard")
        
    with col6:
        charges_annuelles = st.number_input("Charges Copro ANNUELLES (€)", value=1200, help="Montant total par an", key="e_charges")
        taxe_fonciere = st.number_input("Taxe Foncière ANNUELLE (€)", value=917, key="e_tf")

    # --- 4. REVENTE (AMÉLIORATION V11) ---
    st.subheader("4. Revente")
    col7, col8 = st.columns(2)
    
    with col7:
        st.write("**Prix de Revente**")
        mode_revente_expert = st.radio("Saisie Revente", ["Par m² (€/m²)", "Prix Global (€)"], horizontal=True, key="e_mode_revente")
        
        if mode_revente_expert == "Par m² (€/m²)":
            prix_revente_m2_expert = st.number_input("Prix Revente (€/m²)", value=10500, step=100, key="e_rev_m2_input")
            prix_revente_total = surface * prix_revente_m2_expert
            # Affichage dynamique Total
            st.info(f"Soit Total : **{prix_revente_total:,.0f} €**")
        else:
            prix_revente_total = st.number_input("Prix Revente Global (€)", value=520000, step=1000, key="e_rev_global_input")
            # Affichage dynamique m²
            if surface > 0:
                calc_m2_expert = prix_revente_total / surface
                st.info(f"Soit au m² : **{calc_m2_expert:,.0f} €/m²**")

    with col8:
        st.write("**Frais Agence Revente**")
        montant_agence_revente = st.number_input("Montant (€)", value=10000, step=500, key="e_frais_rev")

    # --- 5. MOTEUR DE CALCUL EXPERT ---

    # A. Travaux
    budget_travaux_base = surface * cout_travaux_m2
    honoraires_conducteur = budget_travaux_base * 0.05 
    total_travaux = budget_travaux_base + honoraires_conducteur + architecte + geometre + ingenieur + age_frais + autres_frais_travaux

    # B. Enveloppe Physique
    enveloppe_physique = prix_offre + frais_agence_acq + frais_notaire + total_travaux

    # C. Frais Financiers
    frais_hypotheque = prix_offre * 0.015
    frais_levee = 1500
    duree_totale = duree_mois + retard_mois
    base_portage = enveloppe_physique * 0.75
    interets_portage = base_portage * 0.07 * (duree_totale / 12)
    frais_dossier_banque = 1500 
    total_cout_portage_banque = interets_portage + frais_dossier_banque

    # D. Frais Structure
    frais_sep = enveloppe_physique * 0.02

    # E. Charges
    cout_charges_copro = charges_annuelles * (duree_totale / 12)
    cout_taxe_fonciere = taxe_fonciere * (duree_totale / 12)
    cout_charges_totales = cout_charges_copro + cout_taxe_fonciere

    # F. Total Général
    total_cout_operation = enveloppe_physique + frais_hypotheque + frais_levee + total_cout_portage_banque + frais_sep + cout_charges_totales

    # G. Sortie & Marge
    net_vendeur_reel = prix_revente_total - montant_agence_revente
    total_plus_value = net_vendeur_reel - total_cout_operation
    if total_cout_operation > 0:
        pourcentage_marge = (total_plus_value / total_cout_operation) * 100
    else:
        pourcentage_marge = 0

    # --- AFFICHAGE ---
    st.markdown("---")
    st.header("📊 Bilan Financier Expert")

    c1, c2, c3 = st.columns(3)
    c1.metric("Prix de revente (Brut)", f"{prix_revente_total:,.0f} €")
    c2.metric("Total Coût Opération", f"{total_cout_operation:,.0f} €")
    c3.metric("Total Plus Value", f"{total_plus_value:,.0f} €", delta_color="normal")

    st.markdown(f"### 📈 Rentabilité : **{pourcentage_marge:.2f} %**")

    with st.expander("🔎 Voir le détail des Coûts (Vérification)"):
        st.write(f"**1. Acquisition & Travaux**")
        st.write(f"- Enveloppe Physique (Achat + Notaire 3% + Travaux) : {enveloppe_physique:,.0f} €")
        
        st.write(f"**2. Banque & Garanties**")
        st.write(f"- Portage & Dossier (7% + 1500€) : {total_cout_portage_banque:,.0f} €")
        st.write(f"- Hypothèque (1,5%) : {frais_hypotheque:,.0f} €")
        st.write(f"- Levée Hypothèque : {frais_levee:,.0f} €")
        
        st.write(f"**3. Structure & Vie**")
        st.write(f"- Frais SEP (2%) : {frais_sep:,.0f} €")
        st.write(f"- Charges & Taxe Foncière : {cout_charges_totales:,.0f} €")

    if pourcentage_marge < 25:
        st.error(f"🛑 Marge {pourcentage_marge:.1f}% : Insuffisant")
    elif pourcentage_marge < 40:
        st.warning(f"⚠️ Marge {pourcentage_marge:.1f}% : Standard Partenaire")
    else:
        st.success(f"✅ Marge {pourcentage_marge:.1f}% : Cible Club MOVA")
