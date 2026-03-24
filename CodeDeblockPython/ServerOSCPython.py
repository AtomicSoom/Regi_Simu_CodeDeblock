from pythonosc import dispatcher
from pythonosc import osc_server

# Fonction appelée à la réception du message
def recevoir_valeur(unused_addr, args, valeur):
    print("Valeur reçue de PC B :", valeur)

# Création d’un dispatcher pour écouter l’adresse /valeur
disp = dispatcher.Dispatcher()
disp.map("/velo_start", recevoir_valeur, "velo_start")

# IP et port sur lesquels PC A écoute
ip = "0.0.0.0"   # Écoute sur toutes les interfaces réseau
port = 8001    # Doit correspondre au port choisi dans Unreal

server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
print("Serveur OSC en écoute sur {}:{}".format(ip, port)) 

server.serve_forever()
