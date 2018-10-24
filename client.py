import sys
import socket
import threading
from tkinter import *

MAX_MESSAGES = 50

class Window(Frame):
    def __init__(self, master=None):
      Frame.__init__(self, master)               
      self.master = master
      self.init_window()
      self.message_list = Listbox(master)

    def init_window(self):
      # changing the title of our master widget      
      self.master.title("Chat")

      # allowing the widget to take the full space of the root window
      self.pack(fill=BOTH, expand=1)

      # creating a button instance
      quitButton = Button(self, text="Quit", command=self.client_exit)

      # placing the button on my window
      quitButton.place(x=0, y=0)

    def client_exit(self):
      global client_socket
      print("Connection will now be closed...")
      client_socket.close()
      print("Connection is now closed.")
      exit()

    def addMessage(self, message):
      self.message_list.insert(0, message)
      if self.message_list.size() > 50:
        self.message_list.delete(self.message_list.size()-1)

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
    app.addMessage(readData)
    print(readData)

def print_text():
  global entry
  global client_socket
  data = entry.get() + '\0'
  if data == "!quit\0":
    exit()
  else:
    client_socket.send(data.encode())
    entry.delete(0, END)

def returnKey(event):
  print_text()

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

# Set up GUI
# Initialize window
root = Tk()
root.geometry("400x300")
root.bind("<Return>", returnKey)

app = Window(root)
entry = Entry(root)
entry.pack()
entry.focus_set()

sendButton = Button(root, text="send", command=print_text)
sendButton.pack(side='bottom')

root.mainloop()