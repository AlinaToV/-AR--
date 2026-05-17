import cv2
import numpy as np
import os

dataset_path = 'dataset'

images = [f for f in os.listdir(dataset_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
img_index = 0
frame = None

def nothing(x):
    pass

cv2.namedWindow('Control')
cv2.createTrackbar('H_min', 'Control', 0, 180, nothing)
cv2.createTrackbar('H_max', 'Control', 180, 180, nothing)
cv2.createTrackbar('S_min', 'Control', 0, 255, nothing)
cv2.createTrackbar('S_max', 'Control', 255, 255, nothing)
cv2.createTrackbar('V_min', 'Control', 0, 255, nothing)
cv2.createTrackbar('V_max', 'Control', 255, 255, nothing)

def load_image():
    global frame
    img_path = os.path.join(dataset_path, images[img_index])
    frame = cv2.imread(img_path)
    print(f"изображение {images[img_index]}")

def update():
    if frame is None:
        return
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    h_min = cv2.getTrackbarPos('H_min', 'Control')
    h_max = cv2.getTrackbarPos('H_max', 'Control')
    s_min = cv2.getTrackbarPos('S_min', 'Control')
    s_max = cv2.getTrackbarPos('S_max', 'Control')
    v_min = cv2.getTrackbarPos('V_min', 'Control')
    v_max = cv2.getTrackbarPos('V_max', 'Control')
    
    raw_mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))
    
    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(raw_mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    
    cv2.imshow('Original', frame)
    cv2.imshow('1. Raw Mask', raw_mask)
    cv2.imshow('2. After Opening', opening)
    cv2.imshow('3. After Opening + Closing', closing)

load_image()
update()

while True:
    update()
    
    key = cv2.waitKey(30) & 0xFF
    
    if key == ord('a'):
        img_index = (img_index - 1) % len(images)
        load_image()
    elif key == ord('s'):
        img_index = (img_index + 1) % len(images)
        load_image()
    elif key == ord('q'):
        break

cv2.destroyAllWindows()