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
    "jeux1": {
        "Valeurs fixes": [11, 12, 13, 14, 15, 16],
        "Valeurs spéciales": [21, 22, 23, 24],
        "TEST": list(range(10)),
        "Autres commandes": ["Start", "Stop", "Reset"]
    },
    "jeux2": {
        "Valeurs fixes": [101, 102, 103],
        "Valeurs spéciales": [201, 202],
        "TEST": [0, 1, 2],
        "Autres commandes": ["Play", "Pause"]
    },
    "jeux3": {
        "Valeurs fixes": [7, 8, 9],
        "Valeurs spéciales": [30, 31],
        "TEST": [5, 6, 7],
        "Autres commandes": ["Go", "Stop"]
    }
}
    games={
        "Jeu 1",
        "Jeu 2",
        "Jeu 3"
    }
    
for game_name, game_categories in categories.items():
    with st.expander(game_name): #Expander pour chaque jeu

        for category_name, button_values in game_categories.items():
            with st.expander(category_name):#Expander pour chaque catégorie

                buttons_per_row = 4#Nombre de boutons par ligne

                for start_index in range(0, len(button_values), buttons_per_row):
                    row_buttons = st.columns(buttons_per_row)#Création de colonnes pour les boutons

                    for col_index, button_value in enumerate(button_values[start_index:start_index+buttons_per_row]):
                        with row_buttons[col_index]:#Placement du bouton dans la colonne
                            button_label = str(button_value)#Création du label du bouton à partir de sa valeur

                            key = f"{game_name}_{category_name}_{button_value}_{start_index}_{col_index}"#Clé unique pour chaque bouton afin d'éviter les conflits dans Streamlit

                            if st.button(button_label, key=key):#Action à effectuer lors du clic sur le bouton
                                try:
                                    osc_value = int(button_value)#Conversion de la valeur du bouton en entier pour l'envoyer via OSC
                                except ValueError:
                                    osc_value = button_value#Si la conversion échoue (par exemple pour les commandes textuelles), on garde la valeur telle quelle

                                client.send_message("/valeur", osc_value)#Envoi du message OSC avec l'adresse "/valeur" et la valeur du bouton
                                st.success(f"{button_label} envoyé à {ip}:{port}")#Affichage d'un message de succès pour indiquer que le message OSC a été envoyé