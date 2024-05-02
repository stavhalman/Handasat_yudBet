import socket
import protocol


serverAddress = ('10.0.0.22',8888)

Client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Client.connect(serverAddress)

protocol.sendMessage("takePicture()","do",Client)
protocol.sendMessage('sendMessage("Picture.png","picture",mySocket)',"do",Client)

protocol.reciveMessage(Client)

protocol.showPicture()
