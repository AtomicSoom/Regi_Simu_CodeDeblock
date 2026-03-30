import os
import subprocess

print("=== Lanceur Streamlit ===")

# Dossier où se trouve le .exe
base_dir = os.path.dirname(os.path.abspath(__file__))
print(f"[INFO] Dossier de base : {base_dir}")

# Chemin complet vers le script (même dossier)
script_path = os.path.join(base_dir, "SendToServerOSC.py")
print(f"[INFO] Chemin du script : {script_path}")

if not os.path.isfile(script_path):
    print(f"[ERREUR] Le fichier {script_path} est introuvable !")
    input("Appuie sur Entrée pour quitter...")
    exit(1)

print("[INFO] Lancement de Streamlit...")
subprocess.run(["py", "-m", "streamlit", "run", script_path])
input("Appuie sur Entrée pour fermer...")