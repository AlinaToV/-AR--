import cv2
import os

dataset_path = 'dataset'
images = [f for f in os.listdir(dataset_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

for img_name in images:
    img = cv2.imread(os.path.join(dataset_path, img_name))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"{img_name} | BGR: {img[y,x]} | HSV: {hsv[y,x]}")
    
    cv2.imshow(img_name, img)
    cv2.setMouseCallback(img_name, mouse_callback)
    cv2.waitKey(0)
    cv2.destroyWindow(img_name)
cv2.destroyAllWindows()