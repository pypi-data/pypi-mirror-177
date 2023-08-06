import socket
import sys
import os

def server(ip, port):
    sock.bind((ip, port))
    sock.listen(1)

def client(ip, port,):
    data = True
    try:
        sock.connect((ip,port))
    except:
        data = False
    return data

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

conn_old = None
addr_old = None
class Socket:
    def __init__(self,ip,port,type:str,listen=2):
        self.sock = sock
        self.type = type# 1 for server, 2 for client
        self.data = 'NONE'
        self.data_input = 'NONE'
        self.conn_old = None
        self.addr_old = None
        self.ip = ip
        self.port = port
        self.listen = listen
        self.conns = [0 for i in range(self.listen)]
        self.addrs = [0 for i in range(self.listen)]
        self.conns_old = [0 for i in range(self.listen)]
        self.addrs_old = [0 for i in range(self.listen)]
        self.my_number = 0
        if self.type == "1":
            server(self.ip,self.port)
            self.sock.listen(self.listen)
            for number in range(self.listen):
                self.conns_old[number],self.addrs_old[number] = self.sock.accept()
                print(f'CLIENT {number} connected')
                self.conns_old[number].send(f"{number}".encode())
        elif self.type == "2":
            print(self.ip,self.port)
            self.attempt = client(self.ip,self.port)
            self.my_number = self.data_input = self.sock.recv(1024).decode()
        else:
            print("Invalid input")
            exit(-1)
    def update(self,prinim=1,number_send:int=1): # ret
        if self.data != 'NONE':
            self.conns = self.conns_old
            self.addrs = self.addrs_old
            self.data = str(self.data)
            #print(f'SERVER UPDATE')
            if self.type == "1":
                self.conns[number_send].send(self.data.encode())
                print(f'SERVER {number_send} ACESS TO SEND data send {self.data}')
                if prinim == 1:
                    self.data_input = self.conns[number_send].recv(1024).decode()
            elif self.type == "2":
                sock.send(self.data.encode())
                if prinim == 1:
                    self.data_input = self.sock.recv(1024).decode()
            return self.data_input
    def connect(self,ip,port):
        client(ip,port)