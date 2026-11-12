import copy
import time
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
        self.lost_conection = False
        self.new_frame_event = threading.Event()

    def __del__(self):
        self.disconnect()

    def get_image_aux(self, data):
        if not data or len(data) < 24:
            return None, None, 0, 0, 0
        try:
            np_arr = np.frombuffer(data, np.uint8)
            # Timestamp Data
            timestamp = int.from_bytes(data[-24:-16], "big", signed=False)
            sync_id = int.from_bytes(data[-16:-8], "big", signed=True)
            frame_id = int.from_bytes(data[-8:], "big", signed=True)
            # Image data
            cv2_img = cv2.imdecode(np_arr[:-24], cv2.IMREAD_COLOR)
            im_pil = Image.fromarray(cv2_img) if cv2_img is not None else None
            return im_pil, cv2_img, timestamp, sync_id, frame_id
        except Exception:
            return None, None, 0, 0, 0

    def get_image(self, timeout=2.0):
        if self.lost_conection:
            return None, None, 0, 0, 0

        # Wait for a fresh frame to arrive from the network thread
        got_frame = self.new_frame_event.wait(timeout=timeout)
        self.new_frame_event.clear()

        if not got_frame or self.lost_conection:
            return None, None, 0, 0, 0

        result = self.imageData
        if result is None or len(result) < 2:
            return None, None, 0, 0, 0

        return self.get_image_aux(result[1])

    def receive_images(self):
        try:
            while not self.lost_conection:
                self.imageData = self.myreceive()
                self.new_frame_event.set()
        except Exception:
            self.lost_conection = True
            self.new_frame_event.set()

    def start_image_thread(self):
        self.threadImage = threading.Thread(target=self.receive_images, daemon=True)
        self.threadImage.start()

    def connect(self, host, port):
        self.sock.connect((host, port))

    def disconnect(self):
        self.lost_conection = True
        self.new_frame_event.set()
        try:
            self.sock.shutdown(so.SHUT_RDWR)
        except Exception:
            pass
        try:
            self.sock.close()
        except Exception:
            pass

    def myreceive(self):
        MSGLEN = 0
        max_try = 10
        while MSGLEN == 0 and max_try > 0:
            MSGLEN = int.from_bytes(self.sock.recv(4), byteorder='big')
            max_try -= 1
        if max_try == 0:
            raise Exception('Conenction error')
        data = b''
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 181920))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            data += chunk
            bytes_recd = bytes_recd + len(chunk)
        return (bytes_recd, data)
