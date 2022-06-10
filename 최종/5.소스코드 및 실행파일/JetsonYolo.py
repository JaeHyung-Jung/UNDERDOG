import cv2
import numpy as np
import torch
from playsound import playsound

Object_detector = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt', force_reload=True)

Object_classes = ['Y_Belt', 'N_Belt', 'Y_Collar', 'N_Collar', 'Y_Shoes', 'N_Shoes', 'Y_Helmet', 'N_Helmet']

Object_colors = list(np.random.rand(len(Object_classes),3)*255)

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


# To flip the image, modify the flip_method parameter (0 and 2 are the most common)
print(gstreamer_pipeline(flip_method=0))
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
if cap.isOpened():
    window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
    N_labels = [0, 0, 0, 0] #belt, collar, shoes, helmet
    frames = 0 # frame calculation
    # Window
    while cv2.getWindowProperty("CSI Camera", 0) >= 0:
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 0)
            b, g, r = cv2.split(frame)
            A = cv2.merge([r, g, b])

            # per 10frames
            frames = (frames + 1) % 10

            # detection process
            objs = Object_detector(A)

            # plotting
            for obj in objs.xyxy[0].detach().cpu().numpy():
                # print(obj)
                label = Object_classes[int(obj[5])]  # label text
                if label == 'N_Belt':
                    N_labels[0] = 1
                #elif label == 'N_Collar':
                #    N_labels[1] = 1
                elif label == 'N_Shoes':
                    N_labels[2] = 1
                elif label == 'N_Helmet':
                    N_labels[3] = 1
                score = float(obj[4])
                xmin,ymin,xmax,ymax = map(int, obj[0:4])
                color = Object_colors[Object_classes.index(label)]
                frame = cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 2) 
                frame = cv2.putText(frame, f'{label} ({str(score)})', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, color, 1, cv2.LINE_AA)

        # Sound Output
        if frames == 0 and (N_labels[0] or N_labels[2] or N_labels[3]):
            playsound("beep.mp3")
            N_labels = [0, 0, 0, 0]        

        cv2.imshow("CSI Camera", frame)
        keyCode = cv2.waitKey(30)
        # Save Image
        if keyCode == ord('r'):
            objs.save()
        if keyCode == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    print("Unable to open camera")
