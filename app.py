import streamlit as st

st.set_page_config(page_title="Calculatrice MDB - MOVA", page_icon="🏢", layout="centered")

# ==============================================================================
# CSS SPÉCIAL MOBILE & DESIGN
# ==============================================================================
st.markdown("""
<style>
/* 1. STICKY FOOTER (Barre de rentabilité fixe en bas) */
.fixed-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #ffffff;
    border-top: 1px solid #e5e5e5;
    text-align: center;
    padding: 15px 0;
    z-index: 9999;
    box-shadow: 0px -4px 10px rgba(0,0,0,0.05);
    font-family: sans-serif;
}
.footer-text { font-size: 0.9rem; color: #555; margin-bottom: 2px; text-transform: uppercase; letter-spacing: 1px; }
.footer-value { font-size: 1.6rem; font-weight: 800; }
.safe-zone { height: 120px; } /* Espace vide pour le scroll */

/* 2. Style des boutons radios (Design "Pill") */
div.row-widget.stRadio > div {flex-direction: row; justify-content: center; width: 100%;}
div.row-widget.stRadio > div > label {
    background-color: #ffffff; padding: 8px 12px; border-radius: 20px; margin: 0 4px; 
    cursor: pointer; border: 1px solid #e0e0e0; font-size: 0.85rem; flex-grow: 1; text-align: center;
    transition: all 0.2s;
}
div.row-widget.stRadio > div > label:hover {border-color: #ff4b4b;}
div.row-widget.stRadio > div > label[data-baseweb="radio"] {background-color: #ff4b4b; color: white; border-color: #ff4b4b;}

/* 3. Force l'affichage 2 colonnes sur mobile pour les Metrics */
@media (max-width: 640px) {
    div[data-testid="column"] {
        width: 50% !important;
        flex: 0 0 50% !important;
        min-width: 50% !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("🏢 Calculatrice MDB (V25)")

# Création des onglets
tab_flash, tab_expert = st.tabs(["⚡ FLASH", "🏢 EXPERT"])

# ==============================================================================
# ONGLET 1 : FLASH (DESIGN "CARTES")
# ==============================================================================
with tab_flash:
    
    # --- 1. ACQUISITION ---
    with st.expander("1️⃣ ACQUISITION", expanded=True):
        # Utilisation d'un conteneur avec bordure pour structurer
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                surf_flash = st.number_input("📏 Surface (m²)", value=20.0, step=1.0, key="f_surf")
            with c2:
                prix_flash = st.number_input("💶 Prix Net (€)", value=200000, step=1000, key="f_prix")
            
            # Résultat visuel "Wide" (Large)
            if surf_flash > 0:
                st.markdown("---")
                # Affichage centré et propre du prix au m²
                st.markdown(f"<div style='text-align: center; color: #0068c9; font-weight: bold;'>📍 PRIX ACTUEL : {prix_flash/surf_flash:,.0f} €/m²</div>", unsafe_allow_html=True)

    # --- 2. TRAVAUX ---
    with st.expander("2️⃣ TRAVAUX", expanded=False):
        # Selecteur en haut, hors du cadre
        mode_travaux_flash = st.radio("Estimation :", ["Par m² (€/m²)", "Forfait (€)"], horizontal=True, label_visibility="collapsed", key="f_mode_travaux")
        
        with st.container(border=True):
            c3, c4 = st.columns(2)
            if mode_travaux_flash == "Par m² (€/m²)":
                with c3:
                    cout_m2_flash = st.number_input("Coût/m² (€)", value=2000, step=100, key="f_cout_m2")
                with c4:
                    total_travaux_flash = surf_flash * cout_m2_flash
                    # Metric mise en valeur
                    st.metric("Budget Total", f"{total_travaux_flash/1000:.1f} k€")
            else:
                with c3:
                    total_travaux_flash = st.number_input("Budget (€)", value=40000, step=1000, key="f_total_travaux")
                with c4:
                    if surf_flash > 0:
                        st.metric("Soit au m²", f"{total_travaux_flash/surf_flash:,.0f} €")
                    else:
                        st.metric("Soit au m²", "0 €")

    # --- 3. REVENTE ---
    with st.expander("3️⃣ REVENTE", expanded=False):
        mode_revente_flash = st.radio("Revente :", ["Par m² (€/m²)", "Global (€)"], horizontal=True, label_visibility="collapsed", key="f_mode_revente")
        
        with st.container(border=True):
            c5, c6 = st.columns(2)
            if mode_revente_flash == "Par m² (€/m²)":
                with c5:
                    prix_revente_m2_flash = st.number_input("Revente/m²", value=12000, step=100, key="f_revente_m2")
                with c6:
                    prix_revente_total_flash = surf_flash * prix_revente_m2_flash
                    st.metric("Chiffre d'Aff.", f"{prix_revente_total_flash/1000:.0f} k€")
            else:
                with c5:
                    prix_revente_total_flash = st.number_input("Prix Global", value=340000, step=5000, key="f_revente_global")
                with c6:
                    if surf_flash > 0:
                        st.metric("Soit au m²", f"{prix_revente_total_flash/surf_flash:,.0f} €")

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

    # --- RÉSULTATS INTERMÉDIAIRES (Avant le footer) ---
    st.markdown("### 📊 Synthèse Rapide")
    with st.container(border=True):
        kpi_col1, kpi_col2 = st.columns(2)
        with kpi_col1:
            st.metric("📉 Coût Total", f"{cout_total_flash/1000:.0f} k€", delta="Investi")
        with kpi_col2:
            st.metric("💰 Marge Brute", f"{marge_flash/1000:.0f} k€", delta="Gain")

    # Zone de sécurité pour le scroll
    st.markdown('<div class="safe-zone"></div>', unsafe_allow_html=True)

    # --- STICKY FOOTER ---
    color_renta = "#d9534f" # Rouge
    if renta_flash >= 25: color_renta = "#f0ad4e" # Orange
    if renta_flash >= 40: color_renta = "#28a745" # Vert (Plus vif)

    html_footer = f"""
    <div class="fixed-footer">
        <div class="footer-text">RENTABILITÉ BRUTE</div>
        <div class="footer-value" style="color: {color_renta};">
            {renta_flash:.1f} %
        </div>
    </div>
    """
    st.markdown(html_footer, unsafe_allow_html=True)


# ==============================================================================
# ONGLET 2 : CALCUL EXPERT (BASE V15/V24)
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
            
            frais_notaire = prix_offre * 0.03
            st.info(f"👮‍♂️ Notaire (3%): **{frais_notaire:,.0f} €**")

    st.markdown("---")

    # 2. TRAVAUX & ETUDES
    with st.container():
        st.subheader("2. Travaux & Études")
        type_reno = st.selectbox("Gamme Rénovation", 
                             ["Rafraichissement", "Rénovation Simple", "Lourde", "Luxe"], key="e_type_reno")
        
        tc1,
