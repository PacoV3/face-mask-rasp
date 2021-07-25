from time import sleep, time
from pylepton import Lepton
import numpy as np
import cv2


def capture_photo(wait_time):
    with Lepton() as l:
        frame, _ = l.capture()
    cv2.normalize(frame, frame, 0, 65535, cv2.NORM_MINMAX)
    np.right_shift(frame, 8, frame)
    sleep(wait_time)
    return frame


def main():
    scale_percent = 800
    with Lepton() as l:
        while True:
            frame, _ = l.capture()
            cv2.normalize(frame, frame, 0, 65535, cv2.NORM_MINMAX)
            np.right_shift(frame, 8, frame)
            width = int(80 * scale_percent / 100)
            height = int(60 * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(np.uint8(frame), dim, interpolation = cv2.INTER_AREA)
            cv2.imshow("Frames", resized)
            sleep(0.05)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
            if key == ord("m"):
                name = str(time())
                cv2.imwrite(f'Mask/{name}.png', np.uint8(frame), [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                print(f'Saved Mask Image With Name:{name}')
                sleep(0.5)
            if key == ord("n"):
                name = str(time())
                cv2.imwrite(f'No-Mask/{name}.png', np.uint8(frame), [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                print(f'Saved No-Mask Image With Name:{name}')
                sleep(0.5)

if __name__ == "__main__":
    main()
