import requests
import json
import cv2

addr = 'http://192.168.0.6:5001'
test_url = addr + '/multi_upload'

mask_img = cv2.imread('examples/mask1.jpg')
no_mask_img = cv2.imread('examples/no_mask1.jpg')
h, w = mask_img.shape[:2]
start_X, start_y, end_X, end_y = 10, 0, w - 11, h - 1
_, mask_img_encoded = cv2.imencode('.jpg', mask_img[start_y:end_y, start_X:end_X])
_, no_mask_img_encoded = cv2.imencode('.jpg', no_mask_img[start_y:end_y, start_X:end_X])
# files={'files': ('a.jpg', img_encoded, 'multipart/form-data')}
files = [('files', ('foo.png', mask_img_encoded, 'multipart/form-data')),
        ('files', ('bar.png', no_mask_img_encoded, 'multipart/form-data'))]
response = requests.post(test_url, files=files)
result = json.loads(response.text)
for x in result.items():
	print(x)
