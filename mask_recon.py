print("[INFO] Importing Keras Stuff...")
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
print("[INFO] Importing Other Stuff...")
from pylepton import Lepton
import numpy as np
import time
import cv2

class MaskRecon:
    def __init__(self, coords, model_location):
        print("[INFO] Loading Thermal Model...")
        self.mask_net = load_model(model_location)
        self.coords = coords

    def detect_and_predict_mask(self, frame):
        faces = []
        preds = []
        startX, startY, endX, endY = self.coords
        # ordering, resize it to 224x224, and preprocess it
        face_box = frame[startY:endY, startX:endX]
        face_box = cv2.cvtColor(face_box, cv2.COLOR_BGR2RGB)
        face_box = cv2.resize(face_box, (224, 224))
        face_box = img_to_array(face_box)
        face_box = preprocess_input(face_box)
        cv2.imshow('Preprocess Input',face_box)
        faces.append(face_box)
        faces = np.array(faces, dtype="float32")
        preds = self.mask_net.predict(faces, batch_size=1)
        #             Mask       No mask
        # preds = [[0.00580262 0.99419737]]
        return preds

    def get_mask_p(self, frame, wait_time):
        time.sleep(wait_time)
        #             Mask       No mask
        # preds = [[0.00580262 0.99419737]]
        preds = self.detect_and_predict_mask(frame)
        if preds.any():
            mask, no_mask = preds[0]
            return mask, no_mask
        return -1

def main():
    scale_percent = 800
    mask_recon = MaskRecon(coords=(10, 0, 70, 60), model_location="thermal_mask_detector.model")
    with Lepton() as l:
        while True:
            # Image capture and formatting
            frame, _ = l.capture()
            cv2.normalize(frame, frame, 0, 65535, cv2.NORM_MINMAX)
            np.right_shift(frame, 8, frame)
            # Make the predictions
            mask, no_mask = mask_recon.get_mask_p(frame=frame,wait_time=2)
            # Scale the image
            width = int(80 * scale_percent / 100)
            height = int(60 * scale_percent / 100)
            resized = cv2.resize(np.uint8(frame), (width, height), interpolation = cv2.INTER_AREA)
            # Text stuff
            label = f'Mask: {mask:0.2f}, No Mask:{no_mask:0.2f}'
            cv2.putText(resized, label, (0, height - 10),
			            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("Thermal Frames", resized)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

if __name__ == "__main__":
    main()
