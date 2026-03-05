# app.py
import streamlit as st
from calc import calculer_couverture

# Configuration
st.set_page_config(page_title="Safe-Out", page_icon="🛡️", layout="centered")

st.title("🛡️ Safe-Out")
st.subheader("Le Sniper du Cash-out Optimal")
st.markdown("---")

# --- SIDEBAR : PARAMÈTRES ---
st.sidebar.header("📋 Votre Ticket")
gain_pot = st.sidebar.number_input("Gain potentiel du ticket (€)", min_value=1.0, value=500.0, step=10.0)
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

st.sidebar.markdown("---")
st.sidebar.header("🏦 Comparatif Bookmaker")
offre_cashout = st.sidebar.number_input("Montant Cash-out proposé (€)", min_value=0.0, value=0.0)

# --- CALCULS ET RÉSULTATS ---
resultat, erreur = calculer_couverture(gain_pot, mise_init, cote_couv, strat, pct)

if erreur:
    st.error(erreur)
elif resultat:
    # Affichage des métriques principales
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🎯 MISE À PLACER SUR L'ADVERSAIRE", value=f"{resultat['mise_a_placer']} €")
    with col2:
        st.metric(label="💰 BÉNÉFICE NET ESTIMÉ", value=f"{resultat['benef_moyen']} €")

    # --- VERDICT COMPARATIF ---
    if offre_cashout > 0:
        gain_reel_cashout = offre_cashout - mise_init
        difference = resultat['benef_moyen'] - gain_reel_cashout
        
        st.markdown("### 📢 Verdict Safe-Out")
        if difference > 0:
            st.success(f"✅ **Faites la manipulation manuellement !**")
            st.write(f"En utilisant Safe-Out, vous gagnez **{difference:.2f} € de plus** que le bouton Cash-out.")
            st.caption(f"Le bookmaker tente de vous prendre une commission de {((difference/offre_cashout)*100):.1f}% sur ce rachat.")
        else:
            st.error(f"⚠️ **Le Cash-out est avantageux.**")
            st.write(f"Exceptionnellement, l'offre du bookmaker est meilleure de {abs(difference):.2f} €. Cliquez sur leur bouton.")

    # --- SCÉNARIOS ---
    with st.expander("Voir le détail des scénarios"):
        st.table({
            "Issue": ["Le combiné passe", "La couverture passe"],
            "Bénéfice Net": [f"{resultat['benef_si_combine']} €", f"{resultat['benef_si_couv']} €"]
        })
        st.info(f"Investissement total (Mise init + Couverture) : {resultat['total_investi']} €")

st.markdown("---")
st.caption("Safe-Out : Reprenez le contrôle sur vos paris.")
