import threading
import socket
import os
import pickle, sys
from time import sleep

global linr_alive
linr_alive = False
connections = []
global_hist = []
self_name = ""
self_addr = "SERVER"
self_port = 9999
class Msg(object):
    username = ""
    addr = ""
    text = ""
    def __init__(self, username, addr, text):
        self.username = username
        self.addr = addr
        self.text = text

def distribute(msgobj):
    sendobj = pickle.dumps(msgobj)
    for connection in connections:
        connection[0].send(str.encode(msgobj.text))

def sendMsg(inp):
    txt = Msg(self_name, self_addr, inp)
    global_hist.append(txt)
    distribute(txt)

def sends():
    kill = False
    linr_alive = True
    while True and not kill:
        inp = input()
        try:
            sendMsg(inp)
        except:
            if(kill):
                sys.exit()
            sleep(1)
            print("send failed. Retrying...")
            sendMsg(inp)

def on_connection(connector, addr):
    connections.append((connector, addr))
    print("Connected to IP: " + addr[0] + ":" + str(addr[1]))
    # listener = threading.Thread(target=sendData, ((connector, addr)))
    # listener.start();
    
s = socket.socket()
s.bind(("", 9999))
s.listen(5)
print("Waiting for connections...")
while True:
    conn, addr = s.accept()
    thr = threading.Thread(target=on_connection, args=((conn, addr)))
    thr.start()
    if(not linr_alive):
        thr2 = threading.Thread(target=sends)
        thr2.start()
s.close()