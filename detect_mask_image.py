from take_picture import capture_photo
import requests
import json
import cv2

def predict_thermal_photo(image, url):
    h, w = image.shape[:2]
    start_X, start_y, end_X, end_y = 10, 0, w - 11, h - 1
    # files = [('files', ('foo.png', image[start_y:end_y, start_X:end_X], 'multipart/form-data'))]
    _, encoded_image = cv2.imencode('.jpg', image[start_y:end_y, start_X:end_X])
    files={'files': ('a.jpg', encoded_image, 'multipart/form-data')}
    response = requests.post(url, files=files)
    result = json.loads(response.text)
    if 'data' in result:
        return result['data']
    return -1


def predict_from_image(file_location, url):
    image = cv2.imread(file_location)
    h, w = image.shape[:2]
    start_X, start_y, end_X, end_y = 10, 0, w - 11, h - 1
    _, encoded_image = cv2.imencode('.jpg', image[start_y:end_y, start_X:end_X])
    files = [('files', ('foo.png', encoded_image, 'multipart/form-data'))]
    response = requests.post(url, files=files)
    result = json.loads(response.text)
    if 'data' in result:
        return result['data']
    return -1


def main():
    addr = 'http://192.168.0.6:5001'
    url = addr + '/multi_upload'
    # print(predict_from_image('examples/mask1.jpg', url))
    try:
        while True:
            image = capture_photo(wait_time=0.08)
            result = predict_thermal_photo(image, url)
            print(result,end='\r')
    except KeyboardInterrupt:
        print('\nEnd of program!')

if __name__ == "__main__":
    main()
