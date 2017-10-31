from Client_Server import *
register_peers = {'B':["AB.txt","XY.txt"]}
peers_id ={'B':"127.0.0.1"}
class indexer(threading.Thread):
    def __init__(self,pname,pid,portx): # process name and id
        threading.Thread.__init__(self)
        self.name = pname
        self.id= pid
        self.port=portx
    def registry(self,IP):
        handle = Client(IP,self.port)
        print("client start to registry")
        id = handle.client_recieve(2)
        handle.close_conn()
        id = id.decode("utf-8")
        handle = Client(IP,self.port)
        print("Client start to send filenames")
        filenames = handle.client_recieve_list()
        # add lock here for syncronization
        threadlock.acquire()
        #release lock
        register_peers[id] = filenames # add pair id and the filenames he had
        peers_id[id] = IP
        threadlock.release()
        print("Registry done ",register_peers , peers_id)
        handle.close_conn()
    def search(self,filename):

        peers_list = []
        for key in register_peers:
            for value in register_peers[key]:
               if value == filename:
                   peers_list.append(key)
                   peers_list.append(peers_id[key])
        return peers_list

    def run(self):
        while(1):
            handle = Server(host,self.port)
            print("wait for peer to connect")
            handle.wait_connect()
            need = handle.server_recieve(1024)
            print("client connected and need ",need)
            if(need == "lookup"):
                print("wait for the client to specified the file name")
                handle.wait_connect()
                filename = handle.server_recieve(1024)
                data = indexer.search(self,filename) # search for the filename in the indexer table
                if(data.__len__()==0):
                    print("no file with name ",filename,"wait the client to tell him that")
                    handle.wait_connect()
                    handle.server_send_list("dosn't exist")
                else:
                    print("filname exist wait for the client to send him the peers")
                    handle.wait_connect()
                    handle.server_send_list(data)

            elif(need == "registry"):
                IP = handle.get_IP()
                IP = IP[0] # client address
                handle.close_conn()
                indexer.registry(self,IP)
        print("End of the main")
        handle.close_conn()
try:
    # create lock
    threadlock = threading.Lock()
    client1 = indexer("peer 1",1,porta)
    client2 = indexer("peer 2",2,portb)

    client1.start()
    client2.start()
except Exception as e:
    print(e)