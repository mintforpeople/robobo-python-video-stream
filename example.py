from robobo_video.robobo_video import RoboboVideo
import cv2

videoStream = RoboboVideo("192.168.31.241")

def main():
    print("Starting test app")

    videoStream.connect()

    print("Showing images")
    #rob.setLaneColorInversion(False)
    i = 0
    last_ts = 0
    while True:
        i+=1
        frame, timestamp, sync_id, frame_id = videoStream.getImageWithMetadata()

        if timestamp != last_ts:
            print(timestamp)
            print(sync_id)
            print(frame_id)
            cv2.imshow('smartphone camera', frame)

        last_ts = timestamp
        if cv2.waitKey(1) & 0xFF == ord('q'):
            videoStream.disconnect()
            cv2.destroyAllwindows()
            break


main()
