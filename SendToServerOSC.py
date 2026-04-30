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
    value="192.168.101.46 192.168.101.218"
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
    "VELO": {
    "VITESSE DU VELO": [
        "/velo_cycle1speed",
        "/velo_cycle2speed"
    ],
    "INPUT PLAYER MOVEMENT": [
        "/velo_onJoystick1Left",
        "/velo_onJoystick1Center",
        "/velo_onJoystick1Right",
        "/velo_onJoystick2Left",
        "/velo_onJoystick2Center",
        "/velo_onJoystick2Right"
    ],
    "INPUT PLAYER INTERACTION": [
        "/velo_onButton1",
        "/velo_onButton2"
    ],
    "OPTIONS": [
        "/velo_reset",
        "/velo_start",
        "/velo_close"
    ],
    "CHANGE LA MAP 1": [
        "/velo_setWorld1_1",
        "/velo_setWorld1_2",
        "/velo_setWorld1_3",
        "/velo_setWorld1_4"
    ],
    "CHANGE LA MAP 2": [
        "/velo_setWorld2_1",
        "/velo_setWorld2_2",
        "/velo_setWorld2_3",
        "/velo_setWorld2_4"
    ],
    "CHANGE LA DIFFICULTE": [
        "/velo_setDifficulty1",
        "/velo_setDifficulty2",
        "/velo_setDifficulty3",
        "/velo_setDifficulty4"
    ],
    "VOXEL EVENT": [
        "/velo_voxelEvent1",
        "/velo_voxelEvent2",
        "/velo_voxelEvent3",
        "/velo_voxelEvent4"
    ],
    "MALUS/BONUS": [
        "/velo_onMalus1",
        "/velo_onMalus2",
        "/velo_onBonus1",
        "/velo_onBonus2"
    ]
},
    "MIME": {
    "OPTIONS": [
        "/mime_start",
        "/mime_reset",
        "/mime_close"
    ],
    "VOXEL EVENTS": [
        "/mime_voxelEvent1",
        "/mime_voxelEvent2",
        "/mime_voxelEvent3",
        "/mime_voxelEvent4"
    ],
    "ROBOT": [
        "/mime_robot_head",
        "/mime_robot_leftArm",
        "/mime_robot_rightArm",
        "/mime_robot_legs",
        "/mime_robot_body"
    ],
    "CHICKEN": [
        "/mime_chicken_head",
        "/mime_chicken_leftArm",
        "/mime_chicken_rightArm",
        "/mime_chicken_legs",
        "/mime_chicken_body"
    ],
    "SNOWMAN": [
        "/mime_snowman_head",
        "/mime_snowman_leftArm",
        "/mime_snowman_rightArm",
        "/mime_snowman_legs",
        "/mime_snowman_body"
    ],
    "OCTOPUS": [
        "/mime_octopus_head",
        "/mime_octopus_leftArm",
        "/mime_octopus_rightArm",
        "/mime_octopus_legs",
        "/mime_octopus_body"
    ],
    "CACTUS": [
        "/mime_cactus_head",
        "/mime_cactus_leftArm",
        "/mime_cactus_rightArm",
        "/mime_cactus_legs",
        "/mime_cactus_body"
    ],
    "FRIES": [
        "/mime_fries_head",
        "/mime_fries_leftArm",
        "/mime_fries_rightArm",
        "/mime_fries_legs",
        "/mime_fries_body"
    ],
    "ALIEN": [
        "/mime_alien_head",
        "/mime_alien_leftArm",
        "/mime_alien_rightArm",
        "/mime_alien_legs",
        "/mime_alien_body"
    ],
    "ZOMBIE": [
        "/mime_zombie_head",
        "/mime_zombie_leftArm",
        "/mime_zombie_rightArm",
        "/mime_zombie_legs",
        "/mime_zombie_body"
    ]
},
    "VOXEL": {
        "OPTIONS": [
            "/voxel_reset",
            "/voxel_close",
            ],
        "BEHAVIOR": [
            "voxel_voxelTransition",
            "voxel_voxelEmotion1",
            "voxel_voxelEmotion2",
            "voxel_voxelEmotion3",
            "voxel_voxelEmotion4",
        ]
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