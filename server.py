import socket
import Protocol

# this file runs on the sudpberry pi, the file purpose is to recive orders and execute them
ServerPort=8888
ServerIP='0.0.0.0'

RPISocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
RPISocket.bind((ServerIP,ServerPort))

print("server is up")
RPISocket.listen()
clientSocket,clientAddress = RPISocket.accept()

while True:
    Protocol.receive_message(clientSocket)
    print("done")