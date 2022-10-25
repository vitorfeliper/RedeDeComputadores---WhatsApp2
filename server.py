from datetime import datetime

import socket
import select

currentTime = datetime.now()

PACKAGE_LENGTH = 10
PORT = 5000

serverConection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverConection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverConection.bind(('', PORT))

serverConection.listen()

print("################ WHATSAPP 2 NETWORK ###################")
print("---------------- SERVER INFORMATIONS ------------------")
print("\t\t\t\t\n\n\n\nServer now is running....")
print("\n\n\n\n\n\n\n\nServer conection::::", serverConection.getsockname())
print("[WARNING]: IP ADDRESS WAS HIDDEN!!\n\n\n\n")
print("-------------------------------------------------------")

listSockets = [serverConection]

clients = {}

#======================================= FUNCTION RECEIVE =========================================
def MessageReceive(client_socket):
    try:
        messagePackage = client_socket.recv(PACKAGE_LENGTH)
        if not len(messagePackage):
            return False

        messageLength = int(messagePackage.decode("utf-8").strip()) # decode package received
        return {"header": messagePackage, "data": client_socket.recv(messageLength)} # return package decoded

    except:
        return False # If error then lost package

while True:

    socketRead, _, sockException = select.select(listSockets, [], listSockets)

#================================================ EVENT 0: NEW CONECTION=======================================================================
    for notify in socketRead:
        if notify == serverConection:
            sockClient, clientAddres = serverConection.accept()

            user = MessageReceive(sockClient)
            if user is False:
                continue

            listSockets.append(sockClient)

            clients[sockClient] = user

            print(currentTime, f": New conection from {clientAddres[0]}:{clientAddres[1]} User: {user['data'].decode('utf-8')}")
#============================================================================================================================================


#================================================ EVENT 1: ENDED CONECTION======================================================================
        else:
            msg = MessageReceive(notify)

            if msg is False:
                print(currentTime, f": Conection ended from {clients[notify]['data'].decode('utf-8')}")
                listSockets.remove(notify)
                del clients[notify]
                continue
#============================================================================================================================================

#================================================ EVENT 2: NEW MESSAGE RECEIVED FROM CLIENT==================================================
            user = clients[notify]
            print(currentTime, f": New message from {user['data'].decode('utf-8')}: {msg['data'].decode('utf-8')}")

            for sockClient in clients:
                if sockClient != notify:
                    sockClient.send(user['header'] + user['data'] + msg['header'] + msg['data'])


#================================================================================================================================================
#================================================ CLEAR LIST ====================================================================================
    for notify in sockException:
        listSockets.remove(notify)
        del clients[notify]
#==================================================================================================================================================