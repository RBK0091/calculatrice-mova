import streamlit as st

st.set_page_config(page_title="Calculatrice MDB - MOVA", page_icon="🏢")

st.title("🏢 Calculatrice Rentabilité MDB (V5)")
st.success("Mise à jour : Agence en % & Vocabulaire Fidélite (Plus Value)")
st.markdown("---")

# --- 1. ACQUISITION ---
st.header("1. Acquisition")
col1, col2 = st.columns(2)
with col1:
    surface = st.number_input("Surface (m²)", value=46.6, step=0.1)
    prix_offre = st.number_input("Prix Offre Net Vendeur (€)", value=240000, step=1000)
    
with col2:
    # MODIFICATION : Entrée en % pour les frais d'agence
    taux_agence_acq = st.number_input("Taux Agence Achat (%)", value=0.0, step=0.5, help="Ex: 4% du prix net vendeur")
    frais_agence_acq = prix_offre * (taux_agence_acq / 100)
    if frais_agence_acq > 0:
        st.info(f"Frais Agence : {frais_agence_acq:,.0f} €")
    
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
    architecte = st.number_input("Architecte (MOVA=0€)", value=0)

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
    charges_mensuelles = st.number_input("Charges Copro Mensuelles (€)", value=100)
    taxe_fonciere = st.number_input("Taxe Foncière Annuelle (€)", value=917)

# --- 4. REVENTE ---
st.header("4. Revente")
col7, col8 = st.columns(2)
with col7:
    prix_revente_m2 = st.number_input("Prix Revente estimé (€/m²)", value=10500, step=100)
with col8:
    taux_agence_revente = st.number_input("Taux Agence Revente (%)", value=4.0, step=0.5)

# --- 5. CALCULS DÉTAILLÉS ---

# A. Travaux
budget_travaux_base = surface * cout_travaux_m2
honoraires_conducteur = budget_travaux_base * 0.05 
total_travaux = budget_travaux_base + honoraires_conducteur + architecte + geometre + ingenieur + age_frais + autres_frais_travaux

# B. Enveloppe Physique
enveloppe_physique = prix_offre + frais_agence_acq + frais_notaire + total_travaux

# C. Frais Financiers
# 1. Hypothèque : 1,5% du prix du bien
frais_hypotheque = prix_offre * 0.015
# 2. Levée : Forfait 1500€
frais_levee = 1500
# 3. Bancaires (Portage) : 7% sur 75% de l'enveloppe globale
duree_totale = duree_mois + retard_mois
base_portage = enveloppe_physique * 0.75
frais_bancaires_portage = base_portage * 0.07 * (duree_totale / 12)

# D. Frais Structure
frais_sep = enveloppe_physique * 0.02

# E. Charges
cout_charges = (charges_mensuelles * duree_totale) + (taxe_fonciere * (duree_totale/12))

# F. Total Général
total_cout_operation = enveloppe_physique + frais_hypotheque + frais_levee + frais_bancaires_portage + frais_sep + cout_charges

# G. Sortie & Marge
prix_revente_total = surface * prix_revente_m2
montant_agence_revente = prix_revente_total * (taux_agence_revente / 100)
net_vendeur_reel = prix_revente_total - montant_agence_revente # C'est ce qui rentre vraiment en banque

total_plus_value = net_vendeur_reel - total_cout_operation
pourcentage_marge = (total_plus_value / total_cout_operation) * 100

# --- AFFICHAGE ---
st.markdown("---")
st.header("📊 Bilan Financier")

# MODIFICATION : Affichage Prix de Revente (Brut) & Total Plus Value
c1, c2, c3 = st.columns(3)
c1.metric("Prix de revente", f"{prix_revente_total:,.0f} €")
c2.metric("Total Coût Opération", f"{total_cout_operation:,.0f} €")
c3.metric("Total Plus Value", f"{total_plus_value:,.0f} €", delta_color="normal")

st.markdown(f"### 📈 Rentabilité : **{pourcentage_marge:.2f} %**")

with st.expander("🔎 Voir le détail complet"):
    st.write(f"**Prix Revente (Brut)** : {prix_revente_total:,.0f} €")
    st.write(f"- Frais Agence Revente ({taux_agence_revente}%) : -{montant_agence_revente:,.0f} €")
    st.write(f"= **Net Vendeur Réel** : {net_vendeur_reel:,.0f} €")
    st.write("---")
    st.write(f"**- Total Coût Opération** : -{total_cout_operation:,.0f} €")
    st.write(f"= **Total Plus Value** : {total_plus_value:,.0f} €")
    st.write("---")
    st.write("**Détail des Coûts :**")
    st.write(f"- Enveloppe Physique (Achat+Travaux) : {enveloppe_physique:,.0f} €")
    st.write(f"- Frais Bancaires (Portage 7%) : {frais_bancaires_portage:,.0f} €")
    st.write(f"- Garanties (Hypo + Levée) : {frais_hypotheque + frais_levee:,.0f} €")
    st.write(f"- Frais Structure (SEP 2%) : {frais_sep:,.0f} €")

if pourcentage_marge < 25:
    st.error(f"🛑 Marge {pourcentage_marge:.1f}% : Insuffisant")
elif pourcentage_marge < 40:
    st.warning(f"⚠️ Marge {pourcentage_marge:.1f}% : Standard Partenaire")
else:
    st.success(f"✅ Marge {pourcentage_marge:.1f}% : Cible Club MOVA")
