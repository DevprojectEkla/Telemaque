def server_loop(ip: str, port: int, mode: str):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if not ip:
        ip = "0.0.0.0"
    target = (ip, port)
    server.bind(target)
    server.listen(5)

    print("[*]Server is listening[*]")
    print(f"mode = {mode}")
    print("[*] ....Waiting for client.... [*]")
    # il faut créer un dictionnaire des threads_clients et envoyer tous les futurs messages à tous
    # les clients qui n'ont pas encore émis de message et en tout cas pas au client qui se déconnecte.
    dict_clients = {}
    i = 0

    # on entre dans la boucle d'acceptation de connexion du server
    while True:
        try:

            srv_client_socket, addr = server.accept()  # server.accept() allow a client to
            # connect and returns
            # a tuple of the socket connecting client
            # addr is a tuple containing (ip,port)

            print("[***] Connection accepted: from %s:%d [***]" % (addr[0], addr[1]))
            i += 1
            Thread_Name = f"Client{i}"
            # ici il faut bien faire attention de transférer le nom du thread comme argument au client_handler
            print(dict_clients)
            client_thread = threading.Thread(name=f"Client{i}", target=client_handler,
                                             args=(srv_client_socket, mode, dict_clients,Thread_Name,addr))

            client_thread.start()

            # on récupère tout de suite le nom du nouveau thread et on l'ajoute au dictionnaire

            dict_clients[Thread_Name] = srv_client_socket

            print("[*] New thread started for client %s [*]" % addr[0])
            msg_server = f"[*] New thread started for client {addr[0]}:{addr[1]}[*]"
            data_send = srv_client_socket.send(msg_server.encode("Utf8"))
            print("msg server sent")




        except:
            print("server not responding.. Trying server2")
            server.close()
            i += 1
            if i > 5:
                print("failed after 5 tries shutting down.")
                sys.exit()


def client_handler(srv_client_socket, mode, dict_clients, Thread_Name,addr):
    if srv_client_socket:
        print("client_handler taking over")
        print(dict_clients)

        if mode == "command_shell":
            msg_server = "[*] New session started [*]\n"
            srv_client_socket.send(msg_server.encode("Utf8"))
            print(f"Message:\"{msg_server}\" has been sent to client {srv_client_socket.getpeername()}")
            racine = os.getcwd()
            srv_client_socket.send(racine.encode("Utf8"))

            while True:
                try:
                    
                    cmd_buffer = ""
                    cmd_buffer += srv_client_socket.recv(4092).decode("Utf8")
                    print("receiving from client...")
                    while not len(cmd_buffer):
                        print("still receiving...")
                        cmd_buffer += srv_client_socket.recv(4092).decode("Utf8")
                    # send back the command output
                    print("sending response by returning command")
                    
                    response = run_command(cmd_buffer)
                    # with python3 we need to send bytes only
                    # so we check the type of response
                    # à partir de là il faut s'assurer quel le server n'envoie rien à un thread déconnecté
                    # pour cela on vérifie que son nom n'est pas déjà dans le dictionnaire des connexions (car un thread est à usage unique)
                    for dict_key in dict_clients:
                        if dict_key != Thread_Name:
                            print (cmd_buffer)
                            
                            if isinstance(response, str):
                                response = response.encode("Utf8")

                                try:
                                    dict_clients[dict_key].send(response)
                                    print("response string command sent")
                                except:
                                    print("sending response string over")
                                    srv_client_socket.recv(4092)
                                    print("now receiving...")
                            else:
                                # send back the response
                                try:
                                    dict_clients[dict_key].send(response)
                                    print("response bytes command sent")
                                except:
                                    print("Failed to send response bytes")
                                    srv_client_socket.recv(4092)
                                    break
                        else: 
                            print("envoi du dossier racine") # print de debbugage
                            dict_clients[dict_key].send(racine.encode("Utf8"))
                except:
                    print("client not responding...")
                    server_loop(addr[0],addr[1], mode)

    else:
        print("client not responding, restarting server") # inutile 
        server_loop(ip, mode)


def run_command(cmd):
    print("run command started")

    arg_cmd = shlex.split(cmd)

    if "\\" in arg_cmd:
        output = subprocess.getoutput("echo please don't use \"\\\" to get a change dir cmd. use: '/' instead.")

   
    elif len(arg_cmd) > 1 and "cd" in arg_cmd[0] and os.path.exists(arg_cmd[1]):
        print("Warning: command change directory should not use back slash \\")
        try:
            path = os.path.normpath(arg_cmd[1])
            chdir = os.chdir(path)
            output = os.getcwd()
        except:
            pass
    else:
        try:
            output = subprocess.getoutput(cmd)
            
            try:
                output =  f"{os.getcwd()}" + "\n" + output
        
            except:
                print("tu l'auras pas le cwd !!")
                pass
        
        except:
            output = "Failed to execute command"

    return (output)


if __name__ == '__main__':
    from modules_TLM import *
    server_loop(ip= "127.0.0.1", port= 1234, mode= "command_shell")
        

