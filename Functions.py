import os
import re
import time as timer
import socket as s
import progressbar


def time(socket):
    socket.send(b'time')
    while True:
        print(socket.recv(1024).decode())
        break
    return


def upload(file_name, socket):
    start_time = timer.time()
    file_location = "upload/" + file_name
    try:
        file = open(file_location, "rb")
    except IOError:
        print("No_File")
        return False
    else:
        socket.send(b'upload')
        socket.send(file_name.encode())
        data = socket.recv(1024)
        if not re.match(r'Ok_Name', data.decode()):
            print("Error")
            return False
        size_tm = size = os.stat(file_location).st_size
        size_tm /= pow(2, 20)
        socket.send(bytes(str(size), 'UTF-8'))
        while True:
            data = socket.recv(1024)
            if data:
                break
        data = file.read(1024)
        with progressbar.ProgressBar(max_value=int(size_tm)) as bar:
            while data:
                socket.send(data)
                bar.update(int(file.tell() / pow(2, 20)))
                data = file.read(1024)
        file.close()
        print("Upload speed -", int(size_tm / (timer.time() - start_time)), "mb/s")
        return True


def exit(socket):
    # socket.send(b'exit')
    # while True:
    #     data = socket.recv(1024)
    #     if data:
    #         break
    socket.shutdown(1)
    socket.close()
    return


def download(file_name, socket):
    start_time = timer.time()
    socket.send(b'download')
    socket.send(file_name.encode())
    data = socket.recv(1024)
    if re.match(r'No_File', data.decode()):
        print("no file")
        return False
    file_location = "download/" + file_name
    file = open(file_location, 'wb')
    size_tm = size = int(str(data.decode()))
    size_tm /= pow(2, 20)
    socket.send(b'Ok')
    count = 1024
    with progressbar.ProgressBar(max_value=int(size_tm)) as bar:
        while size > 0:
            download_data = socket.recv(1024)
            file.write(download_data)
            bar.update(int(count / pow(2, 20)))
            size -= len(download_data)
            count += len(download_data)
    file.close()
    print("Download speed -", int(size_tm / (timer.time() - start_time)), "mb/s")
    return True


def hello():
    print("Pls choose command \n echo your_string, time , upload , download or exit\n")
    return


def keepalive(socket, after_idle_sec=1, interval_sec=24, max_fails=5):
    socket.setsockopt(s.SOL_SOCKET, s.SO_KEEPALIVE, 1)
    socket.setsockopt(s.IPPROTO_TCP, s.TCP_KEEPIDLE, after_idle_sec)
    socket.setsockopt(s.IPPROTO_TCP, s.TCP_KEEPINTVL, interval_sec)
    socket.setsockopt(s.IPPROTO_TCP, s.TCP_KEEPCNT, max_fails)
