import streamlit as st

st.set_page_config(page_title="Calculatrice MDB - MOVA", page_icon="🏢", layout="centered")

# CSS Hack pour le style (Boutons radios & Metrics mobile)
st.markdown("""
<style>
/* Style des boutons radios */
div.row-widget.stRadio > div {flex-direction: row; justify-content: center;}
div.row-widget.stRadio > div > label {
    background-color: #f0f2f6; padding: 10px 20px; border-radius: 10px; margin: 0 5px; cursor: pointer; border: 1px solid #d1d5db;
}
div.row-widget.stRadio > div > label[data-baseweb="radio"] {background-color: #ff4b4b; color: white;}

/* Style pour forcer l'affichage côte à côte des metrics sur mobile */
[data-testid="column"] {
    min-width: 0px !important; /* Permet aux colonnes de rétrécir sur mobile */
}
</style>
""", unsafe_allow_html=True)

st.title("🏢 Calculatrice MDB (V22)")

# Création des onglets
tab_flash, tab_expert = st.tabs(["⚡ FLASH (Visite)", "🏢 EXPERT (Détaillé)"])

# ==============================================================================
# ONGLET 1 : CALCUL FLASH (ACCORDÉONS + RÉSULTATS CÔTE À CÔTE)
# ==============================================================================
with tab_flash:
    # --- BLOC 1 : ACQUISITION (Accordéon) ---
    with st.expander("1️⃣ ACQUISITION", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            surf_flash = st.number_input("Surface (m²)", value=20.0, step=1.0, key="f_surf")
        with c2:
            prix_flash = st.number_input("Prix Achat (€)", value=200000, step=1000, key="f_prix")
        
        # Indicateur visuel immédiat
        if surf_flash > 0:
            pm2_flash = prix_flash / surf_flash
            st.info(f"📍 Prix Actuel : **{pm2_flash:,.0f} €/m²**")

    # --- BLOC 2 : TRAVAUX (Accordéon) ---
    with st.expander("2️⃣ TRAVAUX", expanded=True):
        mode_travaux_flash = st.radio("Estimation :", ["Par m² (€/m²)", "Forfait Global (€)"], horizontal=True, label_visibility="collapsed", key="f_mode_travaux")
        
        c3, c4 = st.columns(2)
        
        if mode_travaux_flash == "Par m² (€/m²)":
            with c3:
                cout_m2_flash = st.number_input("Coût/m² (€)", value=2000, step=100, key="f_cout_m2")
            with c4:
                total_travaux_flash = surf_flash * cout_m2_flash
                st.metric("Budget Travaux", f"{total_travaux_flash:,.0f} €")
        else:
            with c3:
                total_travaux_flash = st.number_input("Enveloppe (€)", value=40000, step=1000, key="f_total_travaux")
            with c4:
                if surf_flash > 0:
                    calc_m2_travaux = total_travaux_flash / surf_flash
                    st.metric("Soit au m²", f"{calc_m2_travaux:,.0f} €/m²")
                else:
                    st.metric("Soit au m²", "0 €")

    # --- BLOC 3 : REVENTE (Accordéon) ---
    with st.expander("3️⃣ REVENTE", expanded=True):
        mode_revente_flash = st.radio("Revente :", ["Par m² (€/m²)", "Prix Global (€)"], horizontal=True, label_visibility="collapsed", key="f_mode_revente")
        
        c5, c6 = st.columns(2)
        
        if mode_revente_flash == "Par m² (€/m²)":
            with c5:
                prix_revente_m2_flash = st.number_input("Revente/m²", value=12000, step=100, key="f_revente_m2")
            with c6:
                prix_revente_total_flash = surf_flash * prix_revente_m2_flash
                st.metric("Total Revente", f"{prix_revente_total_flash:,.0f} €")
        else:
            with c5:
                prix_revente_total_flash = st.number_input("Prix Global", value=340000, step=5000, key="f_revente_global")
            with c6:
                if surf_flash > 0:
                    calc_m2_flash = prix_revente_total_flash / surf_flash
                    st.metric("Soit au m²", f"{calc_m2_flash:,.0f} €/m²")

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

    # --- RÉSULTATS COMPACTS (MOBILE) ---
    st.markdown("---")
    
    # Ligne 1 : Coût Total + Marge (Côte à côte)
    kpi_col1, kpi_col2 = st.columns(2)
    with kpi_col1:
        st.metric("📉 Coût Total", f"{cout_total_flash/1000:.0f} k€")
    with kpi_col2:
        st.metric("💰 Marge Brute", f"{marge_flash/1000:.0f} k€")
    
    # Ligne 2 : Rentabilité (Largeur totale pour bien voir)
    if renta_flash < 25:
        st.error(f"🛑 Rentabilité : {renta_flash:.1f} % (Trop faible)")
    elif renta_flash < 40:
        st.warning(f"⚠️ Rentabilité : {renta_flash:.1f} % (Moyen)")
    else:
        st.success(f"🚀 Rentabilité : {renta_flash:.1f} % (Excellent)")


# ==============================================================================
# ONGLET 2 : CALCUL EXPERT (BASE V15 CONSERVÉE)
# ==============================================================================
with tab_expert:
    st.caption("✅ Moteur certifié V14 (Notaire 3% | Portage 7% + Dossier 1500€)")

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
            st.write("Frais d'agence (Achat)")
            mode_agence = st.radio("Saisie Agence", ["%", "Fixe (€)"], horizontal=True, label_visibility="collapsed", key="e_mode_agence")
            
            if mode_agence == "%":
                taux_agence = st.number_input("Taux (%)", value=0.0, step=0.5, key="e_taux_agence")
                frais_agence_acq = prix_offre * (taux_agence / 100)
            else:
                frais_agence_acq = st.number_input("Montant (€)", value=0, step=500, key="e_montant_agence")
            
            # Affichage compact du notaire
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

        # Petits frais sur 3 colonnes pour gagner de la place
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

    # 3. TEMPS & CHARGES (Cote à cote)
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
                prix_revente_m2_expert = st.number_input("Prix/m² (€)", value=10500, step=100, key="e_rev_m2_input")
                prix_revente_total = surface * prix_re
