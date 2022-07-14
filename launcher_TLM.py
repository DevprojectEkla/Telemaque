#! /usr/bin/env python3.10
from client_TLM import client_connexion, start_client

def import_fmodule(filename: str):
    import os
    path = os.getcwd()
    module = open(os.path.join(os.path.normpath(path),filename),"r")
    sortie = module.read()
    return (sortie)

def usage():
    print("Telemaque v.1.0\n")
    print("by Fr. Raphael Boralevi alias Ekla")
    print("inspired by")
    print("Black Hat Pyhton (BHP) Net Tool\n")
    print("Usage: bhpnet.py         -t target_host -p port\n")
    print("-l --listen              -listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run -execute the given file upon receiving a connection")
    print("-c --command             -initialize a command shell\n\n")
    print("-u --upload=destination  -upon receiving connection upload a file and write to [destination]")

    print("Examples:")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c://target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=cat /etc/passwd/")
    print("echo 'ABCDEFGHI'| ./bhpnet.py -t 192.168.0.1 -p 135")
    sys.exit(0)

#def main():
if __name__ == '__main__':
    try:
        # a strange way to import all my modules but it works
        exec(import_fmodule('modules_TLM.py'))  
        exec(import_fmodule('server_TLM.py'))
        exec(import_fmodule('daemon.py'))
        exec(import_fmodule('client_TLM.py'))
        #path = os.getcwd()
        #modules = open(os.path.join(os.path.normpath(path), 'modules_BHP.py'),"r")
        #sortie = modules.read()
        #modules.close()
        #exec(sortie)
           
    except: os.error()
        
    listen  = False
    command = False
    upload  = False
    execute = ""
    target  = ""
    upload_dest = ""
    port = 0


    if not len(sys.argv[1:]):
        
        Default = input("\n\tDo you want to launch the default TLM Server on port 1234 (S), or the TLM Client (C)?")
        
        if Default == 'S':
            server_loop(target="0.0.0.0",port= 1234, mode="command_shell")
            input("enter to continue")
       
        elif Default == 'C':
            target = input("choose a target ip or hostname:")
            port = input("choose a port corresponding to the listening TLM server:")
            start_client(target, port)
            input("enter to continue")
        
        else:
            usage()

    # read the command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port",
                                                                     "command", "upload", ])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_dest = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    # are we going to listen or just send data from stdin?
    if not listen and len(target) and port > 0:
        # read in the buffer from commandline
        # this will block, so send Ctrl-D if not sending input to stdin
        print(f"[*] Connection to {target}:{port} [*]\n")
        input(f"press enter to start the client")

        # send data off
        start_client(target, port)

        # we are going to listen and potentially
        # upload things, execute commands and drop a shell back
        # depending on our commandline options above
    if listen and port!=0: 
        if not command:
            server_loop(target,port,mode="listen only")

        elif command:
        
            print(f"listening mode:{listen}",f"command shell:{command}")
            server_loop(target,port,mode="command_shell")

    else:
        Default = input("\n\tDo you want to launch the default TLM Server on port 1234 (S), or the TLM Client (C)?")
        if Default == 'S':
            server_loop(target="0.0.0.0",port = 1234, mode="command_shell")
        elif Default == 'C':

            target = input("choose a target ip or hostname:")
            port_str = input("choose a port corresponding to the listening TLM server:")
            port = int(port_str)
            
            start_client(target,port) 



        else:
            usage()

# main()
