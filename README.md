# robobo-python-video-stream

This library is required to use the video streaming from the Smartphone's camera in the Robobo.py library. It only runs in Android operating system.

## Installation

Download this repository to your computer and save it in the *robobo.by* folder. Then open a terminal window and type the two following commands:

```
pip install robobopy_videostream
```


## Example

The following script shows an example of the basic usage of this library:

``` python
from robobopy_videostream.RoboboVideo import RoboboVideo
from robobopy.Robobo import Robobo
import cv2
import signal
import sys

IP = "YOUR_IP_GOES_HERE"
rob = Robobo(IP)
videoStream = RoboboVideo(IP)

def cleanup():
    try:
        videoStream.disconnect()
    except:
        pass
    try:
        rob.disconnect()
    except:
        pass
    cv2.destroyAllWindows()
    print("Exited cleanly.")
    sys.exit(0)

def signal_handler(sig, frame):
    cleanup()

signal.signal(signal.SIGINT, signal_handler)

def main():
    print("Starting test app")

    rob.connect()
    videoStream.connect()
    rob.startStream()

    print("Showing images")
    i = 0
    last_ts = 0
    while True:
        i += 1
        frame, timestamp, sync_id, frame_id = videoStream.getImageWithMetadata()
        if timestamp != last_ts:
            print(timestamp, frame_id, sync_id)
        cv2.imshow('smartphone camera', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Escape key
            break
        last_ts = timestamp
    cleanup()

if __name__ == "__main__":
    main()
```