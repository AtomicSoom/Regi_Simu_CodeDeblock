import streamlit as st
from pythonosc import udp_client

# Config OSC
ip = "192.168.101.46"
port = 8001
client = udp_client.SimpleUDPClient(ip, port)

st.title("OSC Control avec Streamlit")
port = st.number_input("Port du serveur OSC", value=port, key="port_input")
ip = st.text_input("Adresse IP du serveur OSC", value="192.168.101.46", key="ip_input")
# Catégorie 1 : Valeurs fixes
with st.expander("Valeurs fixes"):
    if st.button("Envoyer Valeur 11"):
        client.send_message("/valeur", 11)
        st.success(f"Valeur 11 envoyée à {ip}:{port}")

    if st.button("Envoyer Valeur 12"):
        client.send_message("/valeur", 12)
        st.success(f"Valeur 12 envoyée à {ip}:{port}")

# Catégorie 2 : Valeurs personnalisées
with st.expander("Valeurs personnalisées"):
    valeur_personnelle = st.number_input("Envoyer une valeur :", min_value=0, max_value=127, value=0, step=1)
    if st.button("Envoyer valeur personnalisée"):
        client.send_message("/valeur", valeur_personnelle)
        st.success(f"Valeur {valeur_personnelle} envoyée à {ip}:{port}")