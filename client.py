import socket
import protocol


serverAddress = ('10.0.0.22',8888)

UDPClient=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
UDPClient.connect(serverAddress)

protocol.sendMessage("takePicture()","do",UDPClient)
protocol.sendMessage('sendMessage("Picture.png","picture",mySocket)',"do",UDPClient)

protocol.reciveMessage(UDPClient)

protocol.showPicture()
