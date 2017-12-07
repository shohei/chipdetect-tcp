# Echo server program
import socket
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printc(msg):
    print(bcolors.WARNING + msg + bcolors.ENDC)

printc("include matplotlib")
import matplotlib
printc("include numpy")
import numpy as np
printc("include pyplot")
import matplotlib.pyplot as plt


def updatePlot(data):
    print(data)
    printc("plot")
    plt.imshow(data)
    plt.axis("off")
    plt.show()


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while 1:
    conn, addr = s.accept()
    print('Connected by', addr)
    data = conn.recv(2764928)
    if not data: 
        break
    updatePlot(data)
    #conn.sendall("PLOTTING:" + data)
    # update plot
    conn.close()
