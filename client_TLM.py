import socket
import threading

def client_connexion(target_server, mode=""):
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:# connect to our target host
        connexion = client.connect(target_server)
        print(connexion)
        print("*** client connection: ok ***\n") 



        if mode == "standby":
            input(f"Initializing a New session on {target}:{port} :: press enter to continue") # to initialize the connection maybe not necessary at all it was for the debuggage

        if mode == "Recv":
            while True:
                recv_len = 1
                response = ""
                while recv_len: # now wait for data back
                    #print("receiving data from server") # print de debuggage
                    recv_data = client.recv(4096).decode("Utf8")
                    #print("data received") # print de debbugage
                    print(response)
                    recv_len = len(recv_data)
                    response += recv_data

                    if recv_len < 4096:
                        print(response)
                       # print("All data has been received: *** breaking Recvloop ***") # print de debuggage
                        break

                #print(response),

        if mode == "Send":

            while True:
                send_data = input("<hack#>")
                send_data += "\n"

                client.sendall(send_data.encode("Utf8"))
                try:
                    send_enter = "\n"                        
                    client.sendall(send_enter.encode("Utf8"))
                   # print("all data has been send to the client: *** breaking Sendloop ***") # print de debuggage
                except:
                    input("press enter please")
                            
                

    except:
        print("[***] Exception [***]")
        print("[***] Server disconnected: connexion aborted [***]")
        print("disconnecting... ")
        try:            
            client.close()
            print("socket has been successfully closed")
        except socket.error:
            print("attention: echec de la fonction socket.close ... gare aux zombies ::: *_* :::: *_* :::: *_* ::: ")

def start_client(ip, port):
    
    target_server = (ip, port)
    client_connexion(target_server,"standby")
    Reception_Thread = threading.Thread(target=client_connexion, args=(target_server, "Recv"))
    Sending_Thread = threading.Thread(target=client_connexion, args=(target_server, "Send"))
    Reception_Thread.start()
    Sending_Thread.start()

def main():
    start_client(ip,port)

if __name__ == '__main__':
    
    ip = "localhost"
    port = 1234
    start_client(ip,port)


