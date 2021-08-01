from take_picture import Cameras
import requests
import json
import cv2


def send_image(image, url):
    _, encoded_image = cv2.imencode('.jpg', image)
    # Code for sending multiple images/files
    # files = [('files', ('foo.png', encoded_image, 'multipart/form-data'))]
    files = {'files': ('thermal_image.jpg', encoded_image,
                       'multipart/form-data')}
    response = requests.post(url, files=files)
    result = json.loads(response.text)
    if 'data' in result:
        return result['data']
    return -1


def main():
    addr = 'http://192.168.0.6:5001'
    thermal_url = addr + '/thermal_model'
    rgb_url = addr + '/mask_model'
    # thermal_img = cv2.imread('examples/mask1.jpg')
    with Cameras() as cameras:
        # Lepton 2.5 resolution into a squared picture
        start_X, start_y, end_X, end_y = 10, 0, 80 - 11, 60 - 1
        while True:
            thermal_img = cameras.take_thermal_photo()
            thermal_result = send_image(thermal_img[start_y:end_y, start_X:end_X], thermal_url)
            rgb_img = cameras.take_rgb_photo()
            rgb_img = cv2.resize(rgb_img, (224, 224))
            rgb_result = send_image(rgb_img, rgb_url)
            print(f'Thermal: {thermal_result} - RGB: {rgb_result}', end='\r')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Finish')
