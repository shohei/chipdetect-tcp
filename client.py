import numpy as np
import sys

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

# Echo client program
import socket
import sys

printc("include cv2")
import cv2
printc("capture video0")
cap = cv2.VideoCapture(0)
#chips = cv2.imread('chip.png')
printc("read frame")
_,chips= cap.read()
chips_gray = cv2.cvtColor(chips, cv2.COLOR_BGR2GRAY)
printc("blur")
chips_preprocessed = cv2.GaussianBlur(chips_gray, (5, 5), 0)
printc("binarize")
_, chips_binary = cv2.threshold(chips_preprocessed, 120, 255, cv2.THRESH_BINARY)
printc("bitwise NOR")
chips_binary = cv2.bitwise_not(chips_binary)
printc("find contour")
_, chips_contours, _ = cv2.findContours(chips_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
chips_and_contours = np.copy(chips)
min_chip_area = 60
printc("find large contours")
large_contours = [cnt for cnt in chips_contours if cv2.contourArea(cnt) > min_chip_area]

printc("detect rectangle and C.G.")
bounding_img = np.copy(chips)
for contour in large_contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cgx = int(rect[0][0])
        cgy = int(rect[0][1])
        leftx = int(cgx - (rect[1][0]/2.0))
        lefty = int(cgy - (rect[1][1]/2.0))
        angle = round(rect[2],1)
        cv2.drawContours(bounding_img,[box],0,(0,0,255),2)
        cv2.circle(bounding_img,(cgx,cgy), 10, (255,0,0), -1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(bounding_img,'Rot: '+str(angle)+'[deg]',(leftx,lefty), font, 0.7, (0,0,0),2,cv2.LINE_AA)


printc(str(sys.getsizeof(bounding_img)))
HOST = ''    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
#s.sendall(sys.argv[1])
s.sendall(bounding_img)
data = s.recv(1024)
s.close()
print('Received', repr(data))
