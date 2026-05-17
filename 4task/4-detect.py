import cv2
import numpy as np
import os

dataset_path = 'dataset'
images = [f for f in os.listdir(dataset_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
img_index = 0
last_center = None

def nothing(x):
    pass

cv2.namedWindow('Control')
cv2.createTrackbar('H_min', 'Control', 0, 180, nothing)
cv2.createTrackbar('H_max', 'Control', 180, 180, nothing)
cv2.createTrackbar('S_min', 'Control', 0, 255, nothing)
cv2.createTrackbar('S_max', 'Control', 255, 255, nothing)
cv2.createTrackbar('V_min', 'Control', 0, 255, nothing)
cv2.createTrackbar('V_max', 'Control', 255, 255, nothing)

while True:
    frame = cv2.imread(os.path.join(dataset_path, images[img_index]))
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    h_min = cv2.getTrackbarPos('H_min', 'Control')
    h_max = cv2.getTrackbarPos('H_max', 'Control')
    s_min = cv2.getTrackbarPos('S_min', 'Control')
    s_max = cv2.getTrackbarPos('S_max', 'Control')
    v_min = cv2.getTrackbarPos('V_min', 'Control')
    v_max = cv2.getTrackbarPos('V_max', 'Control')
    
    mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))
    
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    result = frame.copy()
    center = None
    
    if contours:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 500:
            (x, y), radius = cv2.minEnclosingCircle(largest)
            center = (int(x), int(y))
            cv2.circle(result, center, int(radius), (0, 255, 0), 2)
    
    if center != last_center:
        if center:
            print(f"центр {center}")
        else:
            print("объект не найден")
        last_center = center
    
    cv2.imshow('Result', result)
    cv2.imshow('Mask', mask)
    
    key = cv2.waitKey(30) & 0xFF
    if key == ord('a'):
        img_index = (img_index - 1) % len(images)
        last_center = None
    elif key == ord('s'):
        img_index = (img_index + 1) % len(images)
        last_center = None
    elif key == ord('q'):
        break

cv2.destroyAllWindows()