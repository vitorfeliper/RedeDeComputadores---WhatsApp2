import socket
from datetime import datetime
import errno
import sys

PACKAGE_LENGTH = 10

local_IP = input("Inform the server ip addres: ")

print("[SERVER MESSAGE]: ALL THE CLIENTS NEEDS THE CLI READER TO BETTER USE")

choose = int(input("Choose option\n1 - CLIENT\n2 - CLIENT_READER\n#######: "))


if choose > 2 or choose < 1 :
	choose = 1

currentTime = datetime.now()

IP = local_IP
PORT = 5000

clientUsername = input("Usuario: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket(var IPv4, var TCP)
client_socket.connect((IP, PORT))

client_socket.setblocking(False) # method


#=========================================  ENCODE USERNAME AND USER DATA ===================================================
username = clientUsername.encode("utf-8")
usernamePackageLength = f"{len(username):<{PACKAGE_LENGTH}}".encode("utf-8")
client_socket.send(usernamePackageLength + username)
#=============================================================================================================================


while True:
	if choose == 1:
		message = input(f"{clientUsername} > ") # client
	elif choose == 2:
		message = "" #reader
	else:
		break

#================== IF user.exists() == true then encode message package===========================================
	if message:
		message = message.encode("utf-8")
		message_header = f"{len(message) :< {PACKAGE_LENGTH}}".encode("utf-8")
		client_socket.send(message_header + message)
#=========================================  ENCODE PACKAGE ========================================================

	try:
		while True:
			usernamePackageLength = client_socket.recv(PACKAGE_LENGTH)

			if not len(usernamePackageLength):
				print(currentTime, ": [SERVER MESSAGE]: Conection ended by server!")
				sys.exit()

#=============================== EVENT 0 =================================================
#						RECEIVE USERNAME AND CLIENT DATA AND DECODE
			username_length_data = int(usernamePackageLength.decode("utf-8").strip())
			username = client_socket.recv(username_length_data).decode("utf-8")
#=============================== EVENT 1 ENDS =================================================

#=============================== EVENT 1 ========================================================
#					RECEIVE MESSAGE DATA AND DECODE
			message_header = client_socket.recv(PACKAGE_LENGTH)
			message_length = int(message_header.decode("utf-8").strip())
#=============================== EVENT 1 ENDS ====================================================

#=============================== EVENT 2 ==========================================================
#					RECEIVE MESSAGE PACKAGE AND DECODE
			message = client_socket.recv(message_length).decode("utf-8")
#=============================== EVENT 2 ENDS ==========================================================

			print(currentTime, f": {username} > {message}") # print message

#============================== EXCEPTIONS ==============================================================
	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print(currentTime, ": ",'[WARNING]: READ ERROR', str(e))
			sys.exit()
		continue

	except Exception as e:
		print(currentTime, ":", '[CRITICAL]: GENERAL ERROR', str(e))
		sys.exit()