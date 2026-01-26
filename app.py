import streamlit as st

# Configuration de la page en mode "wide" pour profiter de la largeur si besoin, mais centré pour mobile
st.set_page_config(page_title="Calculatrice MDB - MOVA", page_icon="🏢", layout="centered")

# CSS pour réduire les marges et optimiser l'espace mobile
st.markdown("""
    <style>
        .block-container {padding-top: 1rem; padding-bottom: 2rem;}
        h1 {font-size: 1.8rem !important; margin-bottom: 0rem;}
        .stMetric {background-color: #f0f2f6; padding: 10px; border-radius: 5px; text-align: center;}
    </style>
""", unsafe_allow_html=True)

st.title("🏢 MOVA | Calculatrice Rentabilité")

# Création des onglets
tab_flash, tab_expert = st.tabs(["⚡ FLASH (Visite)", "🏢 EXPERT (Bureau)"])

# ==============================================================================
# ONGLET 1 : CALCUL FLASH (VISUEL & COMPACT)
# ==============================================================================
with tab_flash:
    # --- BLOC 1 : ACHAT & SURFACE ---
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            surf_flash = st.number_input("Surface (m²)", value=20.0, step=1.0, key="f_surf")
        with c2:
            prix_flash = st.number_input("Prix Achat (€)", value=200000, step=1000, key="f_prix")
        
        # Indicateur Prix m2 discret
        if surf_flash > 0:
            pm2 = prix_flash / surf_flash
            st.caption(f"📍 Prix Achat : **{pm2:,.0f} €/m²**")

    st.markdown("---") 

    # --- BLOC 2 : TRAVAUX & REVENTE (Cote à Cote pour gagner place) ---
    c_input_1, c_input_2 = st.columns(2)
    
    with c_input_1:
        st.write("🛠️ **Travaux**")
        mode_tx = st.selectbox("", ["€/m²", "Forfait €"], key="f_mode_tx", label_visibility="collapsed")
        if mode_tx == "€/m²":
            val_tx = st.number_input("Coût/m²", value=2000, step=100, key="f_val_tx")
            total_tx_flash = surf_flash * val_tx
            st.caption(f"Total: {total_tx_flash/1000:.0f}k€")
        else:
            total_tx_flash = st.number_input("Total (€)", value=40000, step=1000, key="f_val_tx_glob")
            if surf_flash >0: st.caption(f"Soit {total_tx_flash/surf_flash:.0f} €/m²")

    with c_input_2:
        st.write("💰 **Revente**")
        mode_rev = st.selectbox("", ["€/m²", "Total €"], key="f_mode_rev", label_visibility="collapsed")
        if mode_rev == "€/m²":
            val_rev = st.number_input("Prix/m²", value=12000, step=100, key="f_val_rev")
            total_rev_flash = surf_flash * val_rev
            st.caption(f"Total: {total_rev_flash/1000:.0f}k€")
        else:
            total_rev_flash = st.number_input("Total (€)", value=340000, step=5000, key="f_val_rev_glob")
            if surf_flash >0: st.caption(f"Soit {total_rev_flash/surf_flash:.0f} €/m²")

    # --- CALCULS ---
    include_notaire = st.checkbox("Inclure Notaire (3%)", value=False, key="f_not")
    cout_total_flash = prix_flash + total_tx_flash + (prix_flash * 0.03 if include_notaire else 0)
    marge_flash = total_rev_flash - cout_total_flash
    renta_flash = (marge_flash / cout_total_flash * 100) if cout_total_flash > 0 else 0

    # --- BLOC RÉSULTATS (VISUEL) ---
    st.markdown("---")
    
    # Couleur dynamique selon le résultat
    if renta_flash < 25:
        color_box = "red"
        msg = "⛔ TROP FAIBLE"
    elif renta_flash < 40:
        color_box = "orange"
        msg = "⚠️ PARTENAIRE"
    else:
        color_box = "green"
        msg = "🚀 CLUB MOVA"

    # Affichage compact en 3 colonnes métriques
    k1, k2, k3 = st.columns(3)
    k1.metric("Coût Total", f"{cout_total_flash/1000:.0f} k€")
    k2.metric("Marge", f"{marge_flash/1000:.0f} k€")
    k3.metric("Renta %", f"{renta_flash:.1f} %")
    
    st.markdown(f":{color_box}[**VERDICT : {msg}**]")


# ==============================================================================
# ONGLET 2 : EXPERT (ACCORDÉONS POUR ÉVITER LE SCROLL)
# ==============================================================================
with tab_expert:
    
    # --- 1. ACQUISITION (DÉPLIÉ PAR DÉFAUT) ---
    with st.expander("1️⃣ ACQUISITION (Le Bien)", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            surface = st.number_input("Surface (m²)", 46.6, step=0.1, key="e_surf")
            prix_offre = st.number_input("Prix Achat (€)", 240000, step=1000, key="e_prix")
            if surface > 0: st.caption(f"Prix : **{prix_offre/surface:,.0f} €/m²**")
        with c2:
            frais_notaire = prix_offre * 0.03
            st.metric("Notaire (3%)", f"{frais_notaire:,.0f} €")
            
            # Gestion Agence compacte
            mode_ag = st.radio("Agence Achat", ["%", "Fixe"], horizontal=True, label_visibility="collapsed", key="e_mode_ag")
            if mode_ag == "%":
                tx_ag = st.number_input("Taux %", 0.0, step=0.5, key="e_tx_ag")
                frais_agence_acq = prix_offre * (tx_ag/100)
            else:
                frais_agence_acq = st.number_input("Montant €", 0, step=500, key="e_mt_ag")
            if frais_agence_acq > 0: st.caption(f"Agence : {frais_agence_acq:,.0f} €")

    # --- 2. TRAVAUX (FERMÉ PAR DÉFAUT POUR GAIN PLACE) ---
    with st.expander("2️⃣ TRAVAUX & ÉTUDES", expanded=False):
        type_reno = st.selectbox("Type Rénovation", ["Rafraichissement", "Rénovation Simple", "Lourde", "Luxe"], key="e_type")
        
        c3, c4 = st.columns(2)
        with c3:
            cout_tx_m2 = st.number_input("Coût Travaux €/m²", 1500, step=50, key="e_cout_m2")
            architecte = st.number_input("Archi/Suivi (€)", 0, key="e_archi")
        with c4:
            frais_div = st.number_input("Géomètre/Ingé (€)", 2000, help="Geo+Ingé", key="e_div")
            autres_frais = st.number_input("Autres/Permis (€)", 2000, help="AGE+Permis", key="e_autres")

    # --- 3. TEMPS & BANQUE (FERMÉ PAR DÉFAUT) ---
    with st.expander("3️⃣ TEMPS & BANQUE", expanded=False):
        duree_mois = st.slider("Durée (mois)", 3, 18, 10, key="e_duree")
        retard_mois = st.slider("Sécurité Retard", 0, 12, 0, key="e_retard")
        
        c5, c6 = st.columns(2)
        with c5:
            charges_an = st.number_input("Charges Annuelles", 1200, key="e_chg")
        with c6:
            tf_an = st.number_input("Taxe Foncière", 917, key="e_tf")

    # --- 4. REVENTE (DÉPLIÉ) ---
    with st.expander("4️⃣ REVENTE (Sortie)", expanded=True):
        c7, c8 = st.columns(2)
        with c7:
            mode_rev_exp = st.radio("Mode", ["€/m²", "Global"], horizontal=True, label_visibility="collapsed", key="e_mode_rev_exp")
            if mode_rev_exp == "€/m²":
                pm2_rev = st.number_input("Prix Revente €/m²", 10500, step=100, key="e_pm2_rev")
                prix_revente_total = surface * pm2_rev
                st.caption(f"Total : **{prix_revente_total:,.0f} €**")
            else:
                prix_revente_total = st.number_input("Total Revente €", 520000, step=1000, key="e_tot_rev")
                if surface > 0: st.caption(f"Soit **{prix_revente_total/surface:,.0f} €/m²**")
        with c8:
            montant_ag_rev = st.number_input("Agence Revente (€)", 10000, step=500, key="e_ag_rev")

    # --- MOTEUR DE CALCUL (INVISIBLE) ---
    budget_tx_base = surface * cout_tx_m2
    hono_cond = budget_tx_base * 0.05
    total_tx = budget_tx_base + hono_cond + architecte + frais_div + autres_frais
    env_physique = prix_offre + frais_agence_acq + frais_notaire + total_tx
    
    hypo = prix_offre * 0.015
    levee = 1500
    duree_tot = duree_mois + retard_mois
    portage = (env_physique * 0.75) * 0.07 * (duree_tot/12) + 1500
    sep = env_physique * 0.02
    charges = (charges_an + tf_an) * (duree_tot/12)
