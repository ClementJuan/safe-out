# app.py
import streamlit as st
from calc import calculer_couverture

# Configuration
st.set_page_config(page_title="Safe-Out", page_icon="🛡️", layout="centered")

st.title("🛡️ Safe-Out")
st.subheader("L'outil de sécurisation mathématique")
st.markdown("---")

# --- SIDEBAR : PARAMÈTRES ---
st.sidebar.header("📋 Votre Ticket")
gain_pot = st.sidebar.number_input("Gain potentiel du ticket (€)", min_value=1.0, value=500.0, step=10.0)
mise_init = st.sidebar.number_input("Mise initiale déjà placée (€)", min_value=1.0, value=20.0, step=5.0)

# AJOUT : Offre du bookmaker remontée ici
st.sidebar.markdown("---")
st.sidebar.header("🏦 Comparatif Direct")
offre_cashout = st.sidebar.number_input("Offre de rachat du Bookmaker (€)", min_value=0.0, value=0.0, help="Le montant affiché sur votre bouton Cash-out actuel")

st.sidebar.markdown("---")
st.sidebar.header("🎯 Couverture")
cote_couv = st.sidebar.number_input("Cote de l'issue inverse (Couverture)", min_value=1.01, value=2.10, step=0.05)

strat = st.sidebar.selectbox(
    "Stratégie de sécurisation",
    ["Gain Global (Sécurité Totale)", "Mise Uniquement (Breakeven)", "Mise + % de Profit"]
)

pct = 0
if strat == "Mise + % de Profit":
    pct = st.sidebar.slider("% du profit net à garantir", 0, 100, 50)

# --- CALCULS ET RÉSULTATS ---
resultat, erreur = calculer_couverture(gain_pot, mise_init, cote_couv, strat, pct)

if erreur:
    st.error(erreur)
elif resultat:
    # Affichage du Verdict en premier si l'offre bookmaker est saisie
    if offre_cashout > 0:
        gain_reel_cashout = offre_cashout - mise_init
        difference = resultat['benef_moyen'] - gain_reel_cashout
        
        st.markdown("### 📢 Verdict de Rentabilité")
        if difference > 0:
            st.success(f"✅ **Battez le Bookmaker !** En sécurisant manuellement avec Safe-Out, vous gagnez **{difference:.2f} € de plus**.")
            st.info(f"Le bookmaker applique une marge de sécurité de {((difference/offre_cashout)*100):.1f}% à votre désavantage.")
        else:
            st.error(f"⚠️ **Le Cash-out est acceptable.**")
            st.write(f"L'offre du bookmaker est exceptionnellement supérieure de {abs(difference):.2f} €. Profitez-en.")
        st.markdown("---")

    # Métriques de mise
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="📊 MISE À PLACER (Issue Inverse)", value=f"{resultat['mise_a_placer']} €")
    with col2:
        st.metric(label="💰 BÉNÉFICE NET FINAL", value=f"{resultat['benef_moyen']} €")

    # Détails
    with st.expander("Analyse détaillée des gains"):
        st.table({
            "Si votre combiné gagne": [f"{resultat['benef_si_combine']} € NET"],
            "Si la couverture gagne": [f"{resultat['benef_si_couv']} € NET"]
        })
        st.caption(f"Investissement total (Mise ticket + Mise couverture) : {resultat['total_investi']} €")

st.markdown("---")
st.caption("Safe-Out : Ne laissez plus le hasard (ou les bookmakers) décider pour vous.")
