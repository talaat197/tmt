from socket import *
import json
import time
import threading
import ctypes
host = "127.0.0.1"  #indecing server ip
portb = 12345
porta = 12346
portc = 2000
class Client:
    def __init__(self,host,port):
        self.s=socket()
        self.s.connect((host,port))

    def client_send(self,data):
        self.s.send(data.encode('utf-8'))
    def client_recieve(self,length):
        return self.s.recv(1024)
    def client_recievefrom(self,length):
        return self.s.recvfrom(1024)
    def client_recieve_list(self):
        data =  json.loads(self.s.recv(1024).decode('utf-8'))
        return data
    def close_conn(self):
        self.s.close()
    def client_send_list(self,data):
        data=json.dumps(data)
        data = data.encode('utf-8')
        self.s.send(data)


class Server:
    conn = ()
    def __init__(self,host,port):
        self.s=socket()
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind((host,port))
        self.s.listen(5)
    def  wait_connect(self):
        Server.conn = self.s.accept() # conn hold the new connection and the address

    def server_send(self,data):
        Server.conn[0].send(data.encode('utf-8'))

    #retrun ip of the client connected to the server
    def get_IP(self):
        return Server.conn[1]
    def server_send_list(self,data):
        data = json.dumps(data)
        data = data.encode('utf-8')
        Server.conn[0].send(data)

    def server_recieve(self,length):
        return Server.conn[0].recv(length).decode("utf-8")
    def close_conn(self):
        self.s.close()
    def server_recieve_list(self):
        return json.loads(Server.conn[0].recv(1024).decode("utf-8")) #return it to list