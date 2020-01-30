import socket
from threading import Thread
import sys
from time import sleep
import os
s = None
kill = False
hist = []
sender_h = []
def refresh():
    prev_sender = ""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Connected to IP: " + addr[0] + ":" + str(addr[1]))
    print("_______________________________________________")
    for text, i in zip(hist, range(len(hist))):
        if(prev_sender != sender_h[i]):
            print()
            print(sender_h[i] + ": ")
            print("  " + text)
        else:
            print("  " + text)
        prev_sender = sender_h[i]
    

def read_client():
    while True and not kill:
        try:
            d = s.recv(1024) 
            if not d: sys.exit()
            hist.append(d.decode("utf-8"))
            sender_h.append(addr[0])
            refresh()  
        except:
            sleep(1)
            d = conn.recv(1024)   
            if not d: sys.exit()
            hist.append(d.decode("utf-8"))
            sender_h.append(addr[0])
            refresh()
            print("> ", end="")
        
s = socket.socket()
s.bind(("", 9999))
s.listen(5)
conn = 0
conn, addr = s.accept()
print("Connected to IP: " + addr[0] + ":" + str(addr[1]))
print("Wrap commands in %/%.")
recv = Thread(target=read_client)
recv.start()
while True:
    inp = input("> ")
    conn.send(str.encode(inp))
    if(inp == "%quit%"):
        kill = True
        break
    hist.append(inp)
    sender_h.append("You")
    refresh()    
    if(inp == "%cls%"):
       hist = []
       sender_h = []
       refresh()
recv.join()
conn.close()
sys.exit()
 