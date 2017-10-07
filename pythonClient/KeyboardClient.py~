# create an INET, STREAMing socket
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
try:
    s.connect(("localhost", 25000))
    server = "localhost"
    message = ""
    snd = message #Encoding.ASCII.GetBytes(message)

    while (message != "exit" ):
        message = input()
        snd = message.encode("ascii") #Encoding.ASCII.GetBytes(message)
        s.send(snd)
        paluu = s.recv(128)
        print(paluu)
        #sivu = #Encoding.ASCII.GetString(rec, 0, paljon)
        #palaset = sivu.Split()
        #loput = palaset
        #loput = palaset.Skip(1).ToArray()



finally:
    s.close()

"""
paljon = 0
rec = new
byte[256]
snd = Encoding.ASCII.GetBytes(message)
sivu = Encoding.ASCII.GetString(rec, 0, paljon)
"""