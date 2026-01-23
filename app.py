import streamlit as st

st.set_page_config(page_title="Calculatrice MDB - MOVA", page_icon="🏢")

st.title("🏢 Calculatrice Rentabilité MDB (V8)")
st.success("✅ V8 : Ajout indicateur Prix au m² à l'achat")
st.markdown("---")

# --- 1. ACQUISITION ---
st.header("1. Acquisition")
col1, col2 = st.columns(2)
with col1:
    surface = st.number_input("Surface (m²)", value=46.6, step=0.1)
    # MODIFICATION : Intitulé changé
    prix_offre = st.number_input("Prix d'achat (€)", value=240000, step=1000)
    
    # AJOUT DEMANDÉ (V8) : Calcul du prix au m²
    if surface > 0:
        prix_m2_achat = prix_offre / surface
        st.info(f"Prix au m² : {prix_m2_achat:,.0f} €/m²")
    
with col2:
    # MODIFICATION : Choix du mode de saisie pour les frais d'agence
    st.write("Frais d'agence (Achat)")
    mode_agence = st.radio("Mode de saisie", ["En %", "Montant Fixe (€)"], horizontal=True, label_visibility="collapsed")
    
    if mode_agence == "En %":
        taux_agence = st.number_input("Taux Agence (%)", value=0.0, step=0.5)
        frais_agence_acq = prix_offre * (taux_agence / 100)
        if frais_agence_acq > 0:
            st.info(f"Montant : {frais_agence_acq:,.0f} €")
    else:
        frais_agence_acq = st.number_input("Montant Agence (€)", value=0, step=500)
    
    # Notaire 3% (Standard MDB)
    frais_notaire = prix_offre * 0.03
    st.info(f"Frais Notaire (3% MDB) : {frais_notaire:,.0f} €")

# --- 2. TRAVAUX & ETUDES ---
st.header("2. Travaux & Études")
type_reno = st.selectbox("Type de Rénovation", 
                         ["Rafraichissement (400-800€)", "Rénovation Simple (1200-1400€)", "Lourde (1500-1800€)", "Luxe (>2000€)"])

col3, col4 = st.columns(2)
with col3:
    cout_travaux_m2 = st.number_input("Coût Travaux (€/m²)", value=1500, step=50)
    # MODIFICATION : Intitulé changé
    architecte = st.number_input("Architecte et suivi de travaux (€)", value=0)

with col4:
    geometre = st.number_input("Géomètre (€)", value=1000)
    ingenieur = st.number_input("Ingénieur Béton (€)", value=1000)
    age_frais = st.number_input("Frais AGE / RCP (€)", value=2000)
    autres_frais_travaux = st.number_input("Autres (Permis, etc.) (€)", value=0)

# --- 3. PARAMÈTRES TEMPORELS ---
st.header("3. Temps & Charges")
col5, col6 = st.columns(2)
with col5:
    duree_mois = st.slider("Durée projet (mois)", 6, 24, 10)
    retard_mois = st.slider("Marge sécurité retard (mois)", 0, 12, 0)
    
with col6:
    # MODIFICATION : Saisie en Annuel
    charges_annuelles = st.number_input("Charges Copro ANNUELLES (€)", value=1200, help="Montant total par an")
    taxe_fonciere = st.number_input("Taxe Foncière ANNUELLE (€)", value=917)

# --- 4. REVENTE ---
st.header("4. Revente")
col7, col8 = st.columns(2)
with col7:
    prix_revente_m2 = st.number_input("Prix Revente estimé (€/m²)", value=10500, step=100)
with col8:
