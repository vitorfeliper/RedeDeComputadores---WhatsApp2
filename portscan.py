import socket
import sys


# Array of ports to be checked 
ports = [80, 443, 21, 22, 23, 25, 3306, 8080, 8000, 405, 404, 19, 18, 50, 2227, 5000, 3434, 3201, 3333, 6666, 8990, 8090, 20, 43, 402]

# Open TCP protocol and get IPV4 (or a custom IPV4 per argument)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# PORTSCAN
for ports in ports:
	if sock.connect_ex((sys.argv[1], ports)):
		print("PORT: ", ports, " ---- IS OPEN")
	else:
		print("PORT: ", ports, "[WARNING]: IN USE")
sock.close

'''
	Command: portscan.py + seu IP
	Exemple: portscan.py 192.168.0.10
'''