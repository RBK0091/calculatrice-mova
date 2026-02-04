import streamlit as st

st.set_page_config(page_title="Calculatrice MDB - MOVA", page_icon="🏢", layout="centered")

# CSS pour le style (Boutons radios & accordéons)
st.markdown("""
<style>
div.row-widget.stRadio > div {flex-direction: row; justify-content: center;}
div.row-widget.stRadio > div > label {
    background-color: #f0f2f6; padding: 5px 15px; border-radius: 8px; margin: 0 5px; cursor: pointer; border: 1px solid #d1d5db;
}
div.row-widget.stRadio > div > label[data-baseweb="radio"] {background-color: #ff4b4b; color: white;}
/* Style pour compacter les accordéons */
.streamlit-expanderHeader {font-weight: bold; font-size: 1.1rem;}
</style>
""", unsafe_allow_html=True)

st.title("🏢 Calculatrice MDB (V16)")

# Création des onglets
tab_flash, tab_expert = st.tabs(["⚡ FLASH (Temps Réel)", "🏢 EXPERT (Détaillé)"])

# ==============================================================================
# ONGLET 1 : CALCUL FLASH (ACCORDÉONS + SLIDERS)
# ==============================================================================
with tab_flash:
    st.caption("👈 Base V16 : Accordéons & Mixte (Réglettes / Saisie)")

    # --- BLOC 1 : ACQUISITION (Accordeon) ---
    with st.expander("1️⃣ ACQUISITION (Surface & Prix)", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            # Slider pour la surface (plus fluide pour estimer)
            surf_flash = st.slider("Surface (m²)", min_value=10, max_value=200, value=20, step=1, key="f_surf")
        with c2:
            # PRIX : number_input pour pouvoir taper "241680" précisément
            # Le step=5000 permet d'aller vite avec le +/-, mais tu peux taper ce que tu veux.
            prix_flash = st.number_input("Prix Achat (€)", value=200000, step=5000, key="f_prix", help="Tape le montant exact ou utilise +/-")
        
        # Indicateur Prix m²
        if surf_flash > 0:
            pm2_flash = prix_flash / surf_flash
            st.info(f"📍 Prix Achat : **{pm2_flash:,.0f} €/m²**")

    # --- BLOC 2 : TRAVAUX (Accordeon) ---
    with st.expander("2️⃣ TRAVAUX (Estimation)", expanded=True):
        mode_travaux_flash = st.radio("Mode :", ["€/m²", "Forfait €"], horizontal=True, label_visibility="collapsed", key="f_mode_travaux")
        
        if mode_travaux_flash == "€/m²":
            # SLIDER pour effet temps réel sur le coût au m²
            cout_m2_flash = st.slider("Coût Travaux (€/m²)", min_value=0, max_value=3000, value=1500, step=50, key="f_cout_m2")
            total_travaux_flash = surf_flash * cout_m2_flash
            st.write(f"👉 Budget : **{total_travaux_flash:,.0f} €**")
        else:
            # SLIDER pour forfait global
            total_travaux_flash = st.slider("Enveloppe Totale (€)", min_value=0, max_value=200000, value=40000, step=1000, key="f_total_travaux")
            if surf_flash > 0:
                st.write(f"👉 Soit : **{total_travaux_flash/surf_flash:,.0f} €/m²**")

    # --- BLOC 3 : REVENTE (Accordeon) ---
    with st.expander("3️⃣ REVENTE (Objectif)", expanded=True):
        mode_revente_flash = st.radio("Mode :", ["€/m²", "Global €"], horizontal=True, label_visibility="collapsed", key="f_mode_revente")
        
        if mode_revente_flash == "€/m²":
            # SLIDER REVENTE : Pour voir la renta bouger
            prix_revente_m2_flash = st.slider("Revente estimée (€/m²)", min_value=3000, max_value=20000, value=12000, step=100, key="f_revente_m2")
            prix_revente_total_flash = surf_flash * prix_revente_m2_flash
            st.write(f"💰 Total Revente : **{prix_revente_total_flash:,.0f} €**")
        else:
            # ICI : number_input pour pouvoir mettre un prix de revente précis si besoin (ex: Offre reçue)
            prix_revente_total_flash = st.number_input("Prix Global Revente (€)", value=340000, step=5000, key="f_revente_global")
            if surf_flash > 0:
                st.write(f"💰 Soit : **{prix_revente_total_flash/surf_flash:,.0f} €/m²**")

    # --- R
