from robobo_video.my_socket import MySocket


class RoboboVideo:

    def __init__(self, ip):
        self.port = 40405
        self.ip = ip
        self.socket = MySocket()

    def connect(self):
        self.socket.connect(self.ip,self.port)
        self.socket.start_image_thread()

    def getImage(self):
        image, cv2_image, = self.socket.get_image()
        return cv2_image

    def disconnect(self):
        self.socket.disconnect()

