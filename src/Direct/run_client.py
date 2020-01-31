import socket
import sys
from time import sleep
from threading import Thread
import os

kill = False
s = socket.socket()

print("Connected to IP: " + "Server" + ":" + "9999")
print("Wrap commands in %/%.")

global hist
hist = []
sender_h = []

def refresh():
    prev_sender = ""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Connected to IP: " + "Server" + ":" + "9999")
    print("_______________________________________________")
    for text, i in zip(hist, range(len(hist))):
        if(prev_sender != sender_h[i]):
            print()
            print(sender_h[i] + ": ")
            print("  " + text)
        else:
            print("  " + text)
        prev_sender = sender_h[i]
    

def send_txt():
    hist = []
    sender_h = []
    while True and not kill:
        inp = input()
        try:
            s.send(str.encode(inp))
            hist.append(inp)
            sender_h.append("You")
            refresh()    
            if(inp == "%cls%"):
                hist = []
                sender_h = []
                refresh()
        except:
            if(kill):
                sys.exit()
            sleep(1)
            s.send(str.encode(inp)) 
            hist.append(inp)
            sender_h.append("You")
            refresh()    
            if(inp == "%cls%"):
                hist.clear() 
                sender_h.clear()
                refresh()


s.connect(("192.168.0.23", 9999))

sn = Thread(target=send_txt)
sn.start()


while True:
    data = s.recv(1024)
    if(len(data) > 0):
        m = data.decode("utf=8")
        if(m == "%quit%"):
            print("Server has gone offline. Enter enter to exit.")
            kill = True
            s.close()
            sys.exit()
            break
        elif(m == "%cls%"):
            pass
        else:
            hist.append(m)
            sender_h.append("192.168.0.23")
            refresh()
