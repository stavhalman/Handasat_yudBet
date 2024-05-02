from ultralytics import YOLO
import cv2

windowHight = 480
windowLength = 640
# load yolov8 model
model = YOLO('best.pt')
  

  

# load video
video_path = 'Picture.png'
cap = cv2.VideoCapture(0)

ret = True
get = True
# read frames
while ret:
    ret, frame = cap.read()
    if cv2.waitKey(25) & 0xFF == ord('a'):
        get = True
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    if ret:
        if get:

            results = model.track(frame, persist=True)

            frame_ = results[0].plot()
            
            highest = results[0].boxes[0]
            if(len(results[0].boxes) != 0):
                for bx in results[0].boxes:
                    if bx.conf > highest.conf:
                        highest = bx
                print(highest.conf)
                bouldingBoxMiddle = (highest.xyxy[0][0] + highest.xyxy[0][2])/2
                if(bouldingBoxMiddle<=windowLength/3):
                    print("right")
                if(bouldingBoxMiddle>windowLength/3 and bouldingBoxMiddle<windowLength/3*2):
                    print("middle")
                if(bouldingBoxMiddle<=windowLength and bouldingBoxMiddle>=windowLength/3*2):
                    print("left")
            else:
                print("empty")

            #cv2.rectangle(frame_, (75,360),(400,433),(0,255,0),3)

            # visualize
            cv2.imshow('frame', frame_)
            get = False
    else:
        print("smth went wrong")
