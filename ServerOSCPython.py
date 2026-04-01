from pythonosc import dispatcher
from pythonosc import osc_server

# Fonction appelée pour TOUS les messages
def print_all(address, *args):
    print(f"{address} | Args: {args}")

disp = dispatcher.Dispatcher()

# Handler par défaut (catch-all)
disp.set_default_handler(print_all)

ip = "0.0.0.0"
port = 9000

server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
print(f"Serveur OSC en écoute sur {ip}:{port}")

server.serve_forever()