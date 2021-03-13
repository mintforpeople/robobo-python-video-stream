# robobo-python-video-stream

This library is required to use the video streaming from the Smartphone's camera in the Robobo.py library. It only runs in Android operating system.

## Installation

Download this repository to your computer and save it in the *robobo.by* folder. Then open a terminal window and type the two following commands:

```
pip install opencv-python
```

```
pip install pillow
```

## Example

The following script shows an example of the basic usage of this library:

``` python
from robobo_video.robobo_video import RoboboVideo
import cv2

#The IP must be that shown in the Robobo app
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
```