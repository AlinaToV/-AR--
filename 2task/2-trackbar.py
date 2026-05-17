import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('Control')
cv2.createTrackbar('H_min', 'Control', 0, 180, nothing)
cv2.createTrackbar('H_max', 'Control', 180, 180, nothing)
cv2.createTrackbar('S_min', 'Control', 0, 255, nothing)
cv2.createTrackbar('S_max', 'Control', 255, 255, nothing)
cv2.createTrackbar('V_min', 'Control', 0, 255, nothing)
cv2.createTrackbar('V_max', 'Control', 255, 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    h_min = cv2.getTrackbarPos('H_min', 'Control')
    h_max = cv2.getTrackbarPos('H_max', 'Control')
    s_min = cv2.getTrackbarPos('S_min', 'Control')
    s_max = cv2.getTrackbarPos('S_max', 'Control')
    v_min = cv2.getTrackbarPos('V_min', 'Control')
    v_max = cv2.getTrackbarPos('V_max', 'Control')
    
    mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, s_max, v_max))
    
    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()