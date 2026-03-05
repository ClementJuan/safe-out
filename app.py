import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="SAFE-OUT | Gestion de Sorties",
    page_icon="🛡️",
    layout="wide"
)

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .status-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_value=True)

# --- INITIALISATION DES DONNÉES (Session State) ---
if 'check_ins' not in st.session_state:
    st.session_state.check_ins = []

# --- SIDEBAR (Navigation) ---
st.sidebar.title("🛡️ SAFE-OUT")
menu = st.sidebar.radio("Navigation", ["Tableau de bord", "Nouvelle Sortie", "Historique"])

# --- TITRE PRINCIPAL ---
st.title("Système de Sécurité SAFE-OUT")

if menu == "Tableau de bord":
    st.subheader("État actuel de la sécurité")
    
    # Indicateurs rapides
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="status-card"><h4>Sorties Actives</h4><h2>{}</h2></div>'.format(
            len([x for x in st.session_state.check_ins if x['status'] == 'En cours'])
        ), unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="status-card"><h4>Alertes</h4><h2 style="color:red">0</h2></div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="status-card"><h4>Dernier Check-in</h4><p>--:--</p></div>', unsafe_allow_html=True)

    # Graphique d'activité (Mockup)
    if st.session_state.check_ins:
        df = pd.DataFrame(st.session_state.check_ins)
        fig = px.timeline(df, x_start="Heure Départ", x_end="Heure Retour", y="Destination", color="status")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée d'activité pour le moment. Commencez par créer une sortie !")

elif menu == "Nouvelle Sortie":
    st.subheader("Enregistrer une nouvelle sortie")
    
    with st.form("sortie_form"):
        dest = st.text_input("Destination / Activité", placeholder="Ex: Randonnée Col du Chat")
        col_t1, col_t2 = st.columns(2)
        h_dep = col_t1.time_input("Heure de départ", datetime.now().time())
        h_ret = col_t2.time_input("Heure de retour prévue (Alerte)", datetime.now().time())
        contact = st.text_input("Contact d'urgence", value="06 00 00 00 00")
        note = st.text_area("Notes supplémentaires (itinéraire, équipement...)")
        
        submit = st.form_submit_button("Activer la surveillance")
        
        if submit:
            new_entry = {
                "Destination": dest,
                "Heure Départ": datetime.combine(datetime.today(), h_dep),
                "Heure Retour": datetime.combine(datetime.today(), h_ret),
                "Contact": contact,
                "Notes": note,
                "status": "En cours"
            }
            st.session_state.check_ins.append(new_entry)
            st.success(f"Surveillance activée pour {dest} ! Retour prévu à {h_ret}")

elif menu == "Historique":
    st.subheader("Historique des activités")
    if st.session_state.check_ins:
        df_hist = pd.DataFrame(st.session_state.check_ins)
        st.table(df_hist)
    else:
        st.write("L'historique est vide.")

# Pied de page
st.sidebar.markdown("---")
st.sidebar.caption("Interface synchronisée via GitHub. Disponible sur tous vos appareils.")
