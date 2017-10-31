from Client_Server import *
peers_ip = {}
class Peer (threading.Thread):
    def __init__(self,ID,serverport):
        threading.Thread.__init__(self)
        self.id=ID
        self.port=serverport

    def registry(self,id,filenames):
        handler = Server(host,porta)
        str = id
        print("wait for the server to reply")
        handler.wait_connect()
        handler.server_send(str)
        str = filenames
        print("i will send filename")
        handler.wait_connect()
        handler.server_send_list(filenames)
        handler.close_conn()
        print("done registry :)")

    def lookup(self,filename):
        client = Client(host, self.port)
        client.client_send("lookup") # i want to search
        client.close_conn()
        client = Client(host, self.port)
        client.client_send(filename)
        client.close_conn()
        client = Client(host,self.port)
        peerid = client.client_recieve_list()
        self.fill_ip(peerid)
        #print("Peers which had the file u asked is ",peerid)
        client.close_conn()
        return peerid
    def fill_ip(self,peerid):
        i=0
        while(i < len(peerid)):
           peers_ip[peerid[i]] = peerid[i+1]
           del peerid[i+1]
           i=i+1
    def obtain(self,peerip,filename):
        client = Client(peerip,portc)
        print("Sending Filename....")
        client.client_send(filename)
        print("Reciveing ",filename)
        data = client.client_recieve(1024)
        file = open(filename,"w",1)
        file.write(data.decode('utf-8')) # convert byte to string first
        print("Done Recieving")
    def run(self):
        while(1):
            choice = input("Do You want to registry or search ? 1 for registry 2 for search \n")
            if(choice == '1'):
                #send to the server that u want to regstry
                choice = [filename for filename in input("Enter File names split by space\n").split()]
                client = Client(host, 12346)
                client.client_send("registry")  # i want to search
                client.close_conn()
                self.registry(self.id,choice)
            elif(choice =='2'):
                filename = input("Enter Filename Do u need")
                print(filename)
                peerid = self.lookup(filename)
                if(peerid == b"dosn't exist"):
                    print("File Dosn't exist in the server")
                else:
                    print(peerid)
                    choice = input("Choose from one of above peers :")
                    if(choice in peerid):
                        self.obtain(peers_ip[choice],filename)
                    else:
                        print("Choose on of this ",peerid," peers not something else")
            else:
                print("Please choose from 1 or 2 nothing else")
class Peer_server(threading.Thread):
    def __init__(self,id,servport):
        threading.Thread.__init__(self)
        self.ID =id
        self.port = servport
    def get_file(self,filename):
        f = open("Files\\"+filename,"r",1)
        data = f.read()
        return data
    def run(self):
        speer = Server(host,self.port)
        print("Peer wait another peer to connect and ask for file")
        speer.wait_connect()
        filename = speer.server_recieve(1024)
        fdata = self.get_file(filename)
        print("Sending File to the client ....")
        speer.server_send(fdata)
        print("Done sending")
        speer.close_conn()

try:
    clienta = Peer("A",porta)
    #clientb = Peer("B",portb)
    Speer = Peer_server("Peer A",portc)
    clienta.start()
    Speer.start()
except Exception as e:
    print(e)