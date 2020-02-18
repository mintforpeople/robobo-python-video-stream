from robobo_video.robobo_video import RoboboVideo
import cv2

videoStream = RoboboVideo("192.168.31.241")


def main():
    print("Starting test app")

    videoStream.connect()

    print("Showing images")

    while True:
        cv2_image = videoStream.getImage()
        cv2.namedWindow('imagen', cv2.WINDOW_NORMAL)
        cv2.imshow('imagen', cv2_image)
        cv2.waitKey(1)


main()
