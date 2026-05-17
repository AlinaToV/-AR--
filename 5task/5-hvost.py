import cv2
import numpy as np

cap = cv2.VideoCapture(0)
trajectory = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (35, 50, 50), (85, 255, 255))
    
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 500:
            (x, y), r = cv2.minEnclosingCircle(largest)
            center = (int(x), int(y))
            trajectory.append(center)
            if len(trajectory) > 50:
                trajectory.pop(0)
    
    for i in range(1, len(trajectory)):
        alpha = i / len(trajectory)
        thickness = int(1 + alpha * 3)
        color = (0, 0, int(255 * alpha))
        cv2.line(frame, trajectory[i-1], trajectory[i], color, thickness)
    
    cv2.imshow('Trajectory', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()