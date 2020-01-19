import socket


LHOST = socket.gethostbyname(socket.getfqdn())
LPORT = 13057

SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCK.bind((LHOST, LPORT))
SOCK.listen(1)

print(f"Listener on {LHOST}:{LPORT}")
CLIENT, ADDR = SOCK.accept()

while True:
    INPUT_HEADER = CLIENT.recv(1024)
    COMMAND = input(INPUT_HEADER.decode()).encode()
    
    CLIENT.send(COMMAND)
    DATA = CLIENT.recv(1024).decode("utf-8")
    
    if COMMAND is b"":
        print("Please enter a command")
    if DATA == "exit":
        print("Terminating connection", ADDR[0])
        break
    
    print(DATA)

CLIENT.close()
SOCK.close()
