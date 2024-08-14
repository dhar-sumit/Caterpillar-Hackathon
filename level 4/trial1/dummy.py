import cv2
import numpy as np

# Open the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set the width
cap.set(4, 480)  # Set the height

# Load class names
classNames = []
classFile = 'D:/Hackathon/level 4/trial1/coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().strip().split('\n')

# Define paths for configuration and weights
configPath = 'D:/Hackathon/level 4/trial1/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'D:/Hackathon/level 4/trial1/frozen_inference_graph.pb'

# Initialize the DNN model
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Confidence threshold
confThreshold = 0.5

while True:
    success, img = cap.read()
    
    # Check if frame is read correctly
    if not success:
        print("Failed to capture image")
        break
    
    # Perform object detection
    classIds, confs, bbox = net.detect(img, confThreshold=confThreshold)
    
    # Convert the outputs to NumPy arrays if necessary
    if isinstance(classIds, tuple):
        classIds = classIds[0]
    if isinstance(confs, tuple):
        confs = confs[0]
    if isinstance(bbox, tuple):
        bbox = bbox[0]
    
    # Debugging output
    print("Detected classIds:", classIds)
    print("Detected confidences:", confs)
    print("Detected bounding boxes:", bbox)

    # Draw bounding boxes and labels
    if classIds is not None:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            # Ensure classId is within the valid range
            if 1 <= classId <= len(classNames):
                # Convert box coordinates to integers
                x, y, w, h = box
                x, y, w, h = int(x), int(y), int(w), int(h)
                # Draw rectangle on the image
                cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
                # Draw label
                label = f"{classNames[classId - 1].upper()} ({confidence:.2f})"
                cv2.putText(img, label, (x + 10, y + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            else:
                print(f"Detected classId {classId} is out of range. Valid range is 1 to {len(classNames)}.")
    
    # Display the image
    cv2.imshow("Output", img)
    
    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()





############################################
# import cv2

# # img = cv2.imread('D:/Hackathon/level 4/trial1/SUMIT DHAR.jpg')

# cap = cv2.VideoCapture(0)
# cap.set(3,640)
# cap.set(4,480)

# classNames = []
# classFile = 'D:/Hackathon/level 4/trial1/coco.names'

# with open(classFile,'rt') as f:
#     classNames = f.read().rstrip('\n').split('\n')

# configPath = 'D:/Hackathon/level 4/trial1/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
# weightsPath = 'D:/Hackathon/level 4/trial1/frozen_inference_graph.pb'

# net = cv2.dnn_DetectionModel(weightsPath,configPath)
# net.setInputSize(320,320)
# net.setInputScale(1.0/127.5)
# net.setInputMean((127.5,127.5,127.5))
# net.setInputSwapRB(True)

# while True:
#     success, img = cap.read()
#     classIds, confs, bbox = net.detect(img,confThreshold=0.5)
#     print(classIds,bbox)

#     if len(classIds) != 0:
#         for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
#             cv2.rectangle(img,box,color=(0,255,0),thickness=2)
#             cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

#     cv2.imshow("Output",img)
#     cv2.waitKey(0)

###############################################
# import cv2

# # Load the image
# img = cv2.imread('D:/Hackathon/level 4/trial1/SUMIT DHAR.jpg')

# # Resize the image while maintaining the aspect ratio
# def resize_image(image, max_width=800, max_height=600):
#     (h, w) = image.shape[:2]
#     aspect_ratio = w / h

#     # Compute new dimensions
#     if w > max_width or h > max_height:
#         if w > h:
#             new_w = max_width
#             new_h = int(max_width / aspect_ratio)
#         else:
#             new_h = max_height
#             new_w = int(max_height * aspect_ratio)

#         # Resize image
#         resized_image = cv2.resize(image, (new_w, new_h))
#         return resized_image
#     else:
#         return image

# # Resize the image
# img = resize_image(img)

# # Define class names file
# classNames = []
# classFile = 'D:/Hackathon/level 4/trial1/coco.names'

# # Load class names
# with open(classFile, 'rt') as f:
#     classNames = f.read().strip().split('\n')

# # Define paths for configuration and weights
# configPath = 'D:/Hackathon/level 4/trial1/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
# weightsPath = 'D:/Hackathon/level 4/trial1/frozen_inference_graph.pb'

# # Initialize the DNN model
# net = cv2.dnn_DetectionModel(weightsPath, configPath)
# net.setInputSize(320, 320)
# net.setInputScale(1.0 / 127.5)
# net.setInputMean((127.5, 127.5, 127.5))
# net.setInputSwapRB(True)

# # Perform object detection
# classIds, confs, bbox = net.detect(img, confThreshold=0.5)

# # Draw bounding boxes
# if classIds is not None:
#     for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
#         # Convert the bounding box coordinates to integers
#         x, y, w, h = box
#         x, y, w, h = int(x), int(y), int(w), int(h)
#         # Draw rectangle on the image
#         cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

# # Display the image
# cv2.imshow("Output", img)
# cv2.waitKey(0)
cv2.destroyAllWindows()
