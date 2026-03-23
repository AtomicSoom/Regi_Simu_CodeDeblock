from pythonosc import udp_client

ip = "192.168.101.46"
port = 8001

client = udp_client.SimpleUDPClient(ip, port)

client.send_message("/valeur", 11)
print("Valeur 12 envoyée à", ip, ":", port)