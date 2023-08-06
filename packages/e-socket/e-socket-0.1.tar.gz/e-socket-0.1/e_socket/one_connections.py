import socket
import sys
import os

def server(ip, port):
    sock.bind((ip, port))
    sock.listen(1)


def client(ip, port):
    sock.connect((ip, port))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

conn_old = None
addr_old = None
class Socket:
    def __init__(self,ip,port,type:str,listen=2,action_on_disconnect=None):
        self.sock = sock
        self.type = type# 1 for server, 2 for client
        self.data = 'TEST'
        self.data_input = 'STRING'
        self.conn_old = None
        self.addr_old = None
        self.ip = ip
        self.port = port
        self.listen = listen
        self.action_on_disconnect = action_on_disconnect
        if self.type == "1":
            server(self.ip,self.port)
            self.sock.listen(self.listen)
            self.conn_old,self.addr_old = self.sock.accept()
        elif self.type == "2":
            print(self.ip,self.port)
            client(self.ip,self.port)
        else:
            print("Invalid input")
            exit(-1)
    def update(self,prinim=1): # ret
        self.conn = self.conn_old
        self.addr = self.addr_old
        try:
            if self.type == "1":
                self.conn.send(self.data.encode())
                if prinim == 1:
                    self.data_input = self.conn.recv(1024).decode()
            elif self.type == "2":
                sock.send(self.data.encode())
                if prinim == 1:
                    self.data_input = self.sock.recv(1024).decode()
        except:
            '''print('ALL USERS DISCONECTED')
            print('WAIT NEW USERS')
            self.conn_old, self.addr_old = self.sock.accept()'''
            self.action_on_disconnect()
        return self.data_input