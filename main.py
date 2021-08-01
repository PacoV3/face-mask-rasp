from detect_mask_image import send_image
from take_picture import Cameras
from time import sleep, time
import numpy as np
import cv2

def main():
    addr = 'http://192.168.0.6:5001'
    thermal_url = addr + '/thermal_model'
    rgb_url = addr + '/mask_model'
    scale_percent = 600
    with Cameras() as cameras:
        while True:
            thermal_img = cameras.take_thermal_photo()
            start_X, start_y, end_X, end_y = 10, 0, 80 - 11, 60 - 1
            rgb_img = cameras.take_rgb_photo()
            width = int(80 * scale_percent / 100)
            height = int(60 * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(np.uint8(thermal_img), dim, interpolation = cv2.INTER_AREA)
            rgb_show_img = cv2.resize(rgb_img, dim)
            
            thermal_result = send_image(thermal_img[start_y:end_y, start_X:end_X], thermal_url)[0]
            thermal_label = 'Mask: {mask:0.2f}, No Mask:{no_mask:0.2f}'.format(**thermal_result)
            cv2.putText(resized, thermal_label, (0, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("Thermal Camera", resized)

            rgb_api_img = cv2.resize(rgb_img, (224, 224))
            rgb_result = send_image(rgb_api_img, rgb_url)[0]
            rgb_label = 'Mask: {mask:0.2f}, No Mask:{no_mask:0.2f}'.format(**rgb_result)
            cv2.putText(rgb_show_img, rgb_label, (0, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("RGB Camera", rgb_show_img)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("m"):
                name = str(time())
                cv2.imwrite(f'Mask/{name}.png', np.uint8(thermal_img), [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                print(f'Saved Mask Image With Name:{name}')
                sleep(0.5)
            if key == ord("n"):
                name = str(time())
                cv2.imwrite(f'No-Mask/{name}.png', np.uint8(thermal_img), [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                print(f'Saved No-Mask Image With Name:{name}')
                sleep(0.5)

if __name__ == "__main__":
    main()