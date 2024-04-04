import socket
import time
import protocol


ServerPort=8888
ServerIP='0.0.0.0'

RPISocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
RPISocket.bind((ServerIP,ServerPort))

print("server is up")
RPISocket.listen()
clientSocket,clientAddress = RPISocket.accept()


protocol.sendMessage("takePicture()","do",clientSocket)
protocol.sendMessage('sendMessage("Picture.png","picture",mySocket)',"do",clientSocket)

protocol.reciveMessage(clientSocket)
