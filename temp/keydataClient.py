# create an INET, STREAMing socket
import socket
import ctypes
import time

#create an INET, STREAMing socket
serversocket = socket.socket(
socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#bind the socket to a public host,
# and a well-known port

serversocket.bind(("localhost", 25001))
#become a server socket
serversocket.listen(1)
(clientsocket, address) = serversocket.accept()

while 1:
  
  print("silmukka")
  #accept connections from outside
  
  #now do something with the clientsocket
   #in this case, we'll pretend this is a threaded server
  receive = clientsocket.recv(128)
  print(receive) 
  returnmessage = "No moikka moi"
    
  sendback = returnmessage.encode("ascii")
  clientsocket.send(sendback)
 
  


    