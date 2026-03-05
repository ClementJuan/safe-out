# app.py
import streamlit as st
from calc import calculer_couverture

# Configuration Look & Feel
st.set_page_config(page_title="Le Sniper de Cashout", page_icon="🎯", layout="centered")

st.title("🎯 Le Sniper de Cashout")
st.markdown("### Ne laissez plus les bookmakers voler vos gains.")

# --- SIDEBAR : INPUTS ---
st.sidebar.header("📋 Votre Ticket")
gain_pot = st.sidebar.number_input("Gain potentiel du combiné (€)", min_value=1.0, value=500.0, step=10.0)
mise_init = st.sidebar.number_input("Mise initiale déjà placée (€)", min_value=1.0, value=20.0, step=5.0)
cote_couv = st.sidebar.number_input("Cote de l'issue inverse (Couverture)", min_value=1.01, value=2.10, step=0.05)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Stratégie")
strat = st.sidebar.selectbox(
    "Que voulez-vous sécuriser ?",
    ["Gain Global (Sécurité Totale)", "Mise Uniquement (Breakeven)", "Mise + % de Profit"]
)

pct = 0
if strat == "Mise + % de Profit":
    pct = st.sidebar.slider("% du profit à garantir", 0, 100, 50)

# --- CALCULS ---
mise_a_placer, erreur = calculer_couverture(gain_pot, mise_init, cote_couv, strat, pct)

if erreur:
    st.error(erreur)
else:
    # Analyse des résultats
    total_investi = mise_init + mise_a_placer
    benefice_si_couv = (mise_a_placer * cote_couv) - total_investi
    benefice_si_combine = gain_pot - total_investi

    # --- AFFICHAGE DES RÉSULTATS ---
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="🎯 MISE À PLACER", value=f"{mise_a_placer} €")
        st.caption(f"Sur la cote de {cote_couv}")

    with col2:
        benefice_moyen = (benefice_si_couv + benefice_si_combine) / 2
        st.metric(label="💰 BÉNÉFICE ESTIMÉ", value=f"{benefice_moyen:.2f} €")

    # Tableau récapitulatif
    st.markdown("#### Détails des scénarios")
    st.table({
        "Scénario": ["Le combiné passe", "La couverture passe"],
        "Gain Brut": [f"{gain_pot:.2f} €", f"{mise_a_placer * cote_couv:.2f} €"],
        "Frais (Mises)": [f"-{total_investi:.2f} €", f"-{total_investi:.2f} €"],
        "Bénéfice Net": [f"{benefice_si_combine:.2f} €", f"{benefice_si_couv:.2f} €"]
    })

    # Message Marketing "Anti-Arnaque"
    st.warning(f"💡 **Conseil du Sniper** : Si le bookmaker vous propose moins de **{total_investi + (benefice_moyen * 0.8):.2f} €** en Cash-out, ignorez-les et utilisez cette méthode !")
