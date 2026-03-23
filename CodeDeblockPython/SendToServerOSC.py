import streamlit as st
from pythonosc import udp_client

st.title("OSC Control Dynamique avec Streamlit")

# --- Config OSC ---
ip = st.text_input("Adresse IP du serveur OSC", value="192.168.101.46", key="ip_input")
port = st.number_input("Port du serveur OSC", value=8001, step=1, key="port_input")

# Vérification simple IP
try:
    from ipaddress import ip_address
    ip_address(ip)
    valid_ip = True
except ValueError:
    st.error("Adresse IP invalide !")
    valid_ip = False

if valid_ip:
    client = udp_client.SimpleUDPClient(ip, port)

    # --- Catégories et listes de boutons ---
    categories = {
        "Valeurs fixes": [11, 12, 13, 14, 15, 16],
        "Valeurs spéciales": [21, 22, 23, 24],
        "TEST": [0,1,2,3,4,5,6,7,8,9],
        "Autres commandes": ["Start", "Stop", "Reset"]
    }

for category_name, button_values in categories.items():
    # Crée un expander pour la catégorie
    with st.expander(category_name):
        buttons_per_row = 4  # nombre de boutons sur chaque ligne

        # Parcourt les valeurs par tranches pour créer les lignes
        for start_index in range(0, len(button_values), buttons_per_row):
            row_buttons = st.columns(buttons_per_row)

            # Parcourt les boutons de la ligne
            for col_index, button_value in enumerate(button_values[start_index:start_index+buttons_per_row]):
                with row_buttons[col_index]:
                    button_label = str(button_value)

                    if st.button(button_label):
                        # Convertir en entier si possible, sinon garder la valeur telle quelle
                        try:
                            osc_value = int(button_value)
                        except ValueError:
                            osc_value = button_value

                        # Envoie le message OSC
                        client.send_message("/valeur", osc_value)
                        st.success(f"{button_label} envoyé à {ip}:{port}")