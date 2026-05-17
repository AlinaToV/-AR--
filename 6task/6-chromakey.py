import cv2
import numpy as np
import os

dataset_path = 'dataset'

background = cv2.imread(os.path.join(dataset_path, 'fon.jpg'))

images = [f for f in os.listdir(dataset_path) if f.endswith(('.jpg', '.png', '.jpeg')) and f != 'fon.jpg']
img_index = 0

while True:
    frame = cv2.imread(os.path.join(dataset_path, images[img_index]))
    
    if frame.shape != background.shape:
        background = cv2.resize(background, (frame.shape[1], frame.shape[0]))
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (35, 50, 50), (85, 255, 255))
    
    frame[mask > 0] = background[mask > 0]
    
    cv2.imshow('Chroma Key', frame)
    
    key = cv2.waitKey(0) & 0xFF
    
    if key == ord('a'):
        img_index = (img_index - 1) % len(images)
    elif key == ord('s'):
        img_index = (img_index + 1) % len(images)
    elif key == ord('q'):
        break

cv2.destroyAllWindows()