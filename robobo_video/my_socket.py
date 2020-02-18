import copy
import socket as so
import threading
import cv2
import numpy as np
from PIL import Image


class MySocket:

    def __init__(self, sock=None):

        if sock is None:
            self.sock = so.socket(so.AF_INET, so.SOCK_STREAM)
            self.sock.setsockopt(so.SOL_SOCKET, so.SO_SNDBUF, 181920)  # Buffer size 8192
        else:
            self.sock = sock

        self.imageData = None
        self.threadImage = None
        self.loss_conextion = False

    def __del__(self):
        self.disconnect();

    def get_image_aux(self, data):
        np_arr = np.frombuffer(data, np.uint8)
        cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        im_pil = Image.fromarray(cv2_img)
        return im_pil, cv2_img

    def get_image(self):
        result = None
        while result is None and self.loss_conextion is False:
            result = copy.copy(self.imageData)
        return self.get_image_aux(result[1])

    def receive_images(self):
        try:
            while True:
                self.imageData = self.myreceive()
        except:
            self.loss_conextion = True

    def start_image_thread(self):
        self.threadImage = threading.Thread(target=self.receive_images)
        self.threadImage.start()

    def connect(self, host, port):
        self.sock.connect((host, port))

    def disconnect(self):
        self.sock.close()

    def myreceive(self):
        MSGLEN = 0
        max_try = 10
        while MSGLEN == 0 and max_try > 0:
            MSGLEN = int.from_bytes(self.sock.recv(4), byteorder='big')
            max_try -= 1
        if max_try == 0:
            raise Exception('Error en la conexio')
        data = b''
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 181920))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            data += chunk
            bytes_recd = bytes_recd + len(chunk)
        return (bytes_recd, data)
