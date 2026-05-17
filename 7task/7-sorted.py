import cv2
import numpy as np
import os

dataset_path = 'dataset'
images = [f for f in os.listdir(dataset_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
img_index = 0

while True:
    frame = cv2.imread(os.path.join(dataset_path, images[img_index]))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    red1 = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
    red2 = cv2.inRange(hsv, (170, 100, 100), (180, 255, 255))
    red = cv2.bitwise_or(red1, red2)
    green = cv2.inRange(hsv, (35, 50, 50), (85, 255, 255))
    blue = cv2.inRange(hsv, (100, 50, 50), (130, 255, 255))
    
    kernel = np.ones((5,5), np.uint8)
    
    counts = {}
    colors_data = [('red', red, (0, 0, 255)), ('green', green, (0, 255, 0)), ('blue', blue, (255, 0, 0))]
    
    for name, mask, bgr in colors_data:
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        count = 0
        for cnt in contours:
            if cv2.contourArea(cnt) > 200:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x+w, y+h), bgr, 2)
                count += 1
        counts[name] = count
        cv2.putText(frame, f'{name}: {count}', (10, 30 + 30 * ['red', 'green', 'blue'].index(name)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, bgr, 2)
    
    cv2.imshow('Sorter', frame)
    
    key = cv2.waitKey(0) & 0xFF
    if key == ord('a'): img_index = (img_index - 1) % len(images)
    elif key == ord('s'): img_index = (img_index + 1) % len(images)
    elif key == ord('q'): break

cv2.destroyAllWindows()