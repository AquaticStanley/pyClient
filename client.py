import sys
import socket
import threading

#DEBUG
HOST = ""
PORT = 0000
USERNAME = ''
IP = "0.0.0.0"
MAX_MESSAGE_LENGTH = 768
MAX_USERNAME_LENGTH = 256

def assignConstants():
  global HOST
  global PORT
  global USERNAME
  global IP
  config = open("Profile.cfg")
  config.readline()
  USERNAME = config.readline().strip()
  config.readline()
  config.readline()
  HOST = config.readline().strip()
  config.readline()
  config.readline()
  IP = config.readline().strip()
  config.readline()
  config.readline()
  PORT = int(config.readline().strip())
  config.close()

def readthread(client_socket):
  while True:
    readData = ''
    readData = client_socket.recv(1024)
    readData = readData.decode('utf-8',errors='ignore')
    readData = readData.split('\0')[0]
    print(readData)

# Populate constants
assignConstants()

# Create Socket
print("Creating socket...", end="")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Success!")

# Connect to host
print("Connecting to host...", end="")
client_socket.connect((IP, PORT))
print("Success!")

# Send username to use
client_socket.send((USERNAME + '\0').encode())

# Make new thread to read on
read_thread = threading.Thread(target=readthread, args = (client_socket,))
read_thread.setDaemon(True)
read_thread.start()

while True:
  data = input() + '\0';
  if data == "!quit\0":
    break
  else:
    client_socket.send(data.encode())

print("Connection will now be closed...")
client_socket.close()
print("Connection is now closed.")