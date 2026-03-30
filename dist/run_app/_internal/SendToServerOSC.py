import streamlit as st
from pythonosc import udp_client
from ipaddress import ip_address

import re

def format_string(s: str) -> str:
    # Supprimer le préfixe jusqu'au premier underscore
    parts = s.split('_', 1)
    if len(parts) < 2:
        return s  # au cas où le format est inattendu
    
    core = parts[1]  # "setWorld1_3"
    
    # Séparer la partie texte et le nombre final
    #match = re.match(r'([a-zA-Z]+\d*)_(\d+)', core)
    #if not match:
    #    return core
    
    #text_part = match.group(1)
    #number_part = match.group(2)
    
    # Mettre la première lettre en majuscule
    #text_part = text_part.capitalize()
    text_part = core.capitalize()
    
    #return f"{text_part} {number_part}"
    return f"{text_part}"


#s = "velo_setWorld1_3"
#print(format_string(s))


st.title("OSC Control Dynamique avec Streamlit")

# --- Config OSC ---
ips_input = st.text_input(
    "Adresses IP (séparées par des virgules)",
    value="192.168.101.46 192.168.101.218 192.168.101.35"
)
port = st.number_input("Port du serveur OSC", value=8001, step=1)

ips = [ip.strip() for ip in ips_input.split(" ")]

clients = []
valid_ips = []

for ip in ips:
    try:
        ip_address(ip)
        clients.append(udp_client.SimpleUDPClient(ip, port))
        valid_ips.append(ip)
    except ValueError:
        st.error(f"IP invalide : {ip}")

    # --- Catégories et listes de boutons ---
    categories = {
    "jeux1": {
        "Velo": ["velo_setWorld1_3", "velo_setWorld2_1", "velo_start", "Velo_4", "Velo_5", "Velo_6"],
        "Valeurs spéciales": ["TEST"],
        "TEST": ["TEST1", "TEST2", "TEST3"],
        "Autres commandes": ["Start", "Stop", "Reset"]
    },
    "jeux2": {
        "Valeurs fixes": ["Start", "Start", "Start"],
        "Valeurs spéciales": ["TEST"],
        "TEST": ["TEST1", "TEST2", "TEST3"],
        "Autres commandes": ["Play", "Pause"]
    },
    "jeux3": {
        "Valeurs fixes": ["Go", "Go", "Go"],
        "Valeurs spéciales": ["TEST"],
        "TEST": ["TEST1", "TEST2", "TEST3"],
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
                            button_label = format_string(button_value)#Création du label du bouton à partir de sa valeur

                            key = f"{game_name}_{category_name}_{button_value}_{start_index}_{col_index}"#Clé unique pour chaque bouton afin d'éviter les conflits dans Streamlit

                            if st.button(button_label, key=key):#Action à effectuer lors du clic sur le bouton
                                try:
                                    osc_value = int(button_value)#Conversion de la valeur du bouton en entier pour l'envoyer via OSC
                                except ValueError:
                                    osc_value = button_value#Si la conversion échoue (par exemple pour les commandes textuelles), on garde la valeur telle quelle

                                for client, ip in zip(clients, valid_ips):
                                    client.send_message("/" + str(osc_value), osc_value)
                                st.success(f"/{osc_value} envoyé à {len(clients)} clients")