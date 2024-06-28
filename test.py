import cv2

cam = cv2.VideoCapture(0)
i = 0
while True:
    while cv2.waitKey('space'):
        pass
    result,image = cam.read()
    if result:
        cv2.imwrite(str(i),image)