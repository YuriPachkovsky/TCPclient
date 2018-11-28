import re
import socket as sock
import Functions

socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
Functions.keepalive(socket)
socket.connect(('192.168.43.18', 3000))

while True:
    try:
        Functions.hello()
        data_choose = input()
        if re.match(r'exit', data_choose):
            Functions.exit(socket)
            break
        elif re.match(r'echo ', data_choose):
            socket.sendall(data_choose.encode())
            rec_data = socket.recv(1024).decode()
            while rec_data[len(rec_data) - 1] != '\n':
                print(rec_data.strip())
                rec_data = socket.recv(1024).decode()
            print(rec_data.strip())
            continue
        elif re.match(r'time', data_choose):
            socket.send(data_choose.encode())
            rec_data = socket.recv(1024)
            print(rec_data.decode().strip())
            continue
        elif re.match(r'upload', data_choose):
            print("pls input file name")
            name_up = input()
            if Functions.upload(name_up, socket):
                print("\n")
            continue
        elif re.match(r'download', data_choose):
            print("pls input file name")
            name_dw = input()
            if Functions.download(name_dw, socket):
                print("\n")
            continue
        else:
            print('Invalid command. Please enter: echo, time, exit, download, upload\n')
    except TimeoutError:
        print("TimeoutError : pls choose \n 1 - terminate \n 2 - wait")
        ch = input()
        if ch == '1':
            socket.close()
            break
        else:
            continue
