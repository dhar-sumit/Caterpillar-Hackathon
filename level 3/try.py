# Paths to YOLO files
# weights_path = "D:/Hackathon/level 3/yolov3.weights"
# cfg_path = "D:/Hackathon/level 3/yolov3.cfg"
# names_path = "D:/Hackathon/level 3/coco.names"
# image_path = "D:/Hackathon/level 3/tyre1.jpg"


import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# Paths to YOLO files
weights_path = "D:/Hackathon/level 3/yolov3.weights"
cfg_path = "D:/Hackathon/level 3/yolov3.cfg"
names_path = "D:/Hackathon/level 3/coco.names"
image_path = "D:/Hackathon/level 3/tyre1.jpg"

# Check if files exist
if not (os.path.exists(weights_path) and os.path.exists(cfg_path) and os.path.exists(names_path)):
    raise FileNotFoundError("One or more YOLO files are missing. Please check the paths.")

# Load YOLO
net = cv2.dnn.readNet(weights_path, cfg_path)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Define the 10 objects you want to detect
object_names = [
    "person", "bicycle", "car", "motorbike", "aeroplane",
    "bus", "train", "truck", "boat", "traffic light"
]

# Load COCO names and filter for the selected objects
with open(names_path, "r") as f:
    coco_names = [line.strip() for line in f.readlines()]

selected_indices = [coco_names.index(name) for name in object_names if name in coco_names]

def detect_objects(image_path):
    # Load image
    img = cv2.imread(image_path)
    height, width, channels = img.shape

    # Prepare image for YOLO
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    # Debug: Print the shapes of output layers
    for i, out in enumerate(outs):
        print(f"Output layer {i} shape: {out.shape}")

    # Process detections
    for out in outs:
        for detection in out:
            print(f"Detection shape: {detection.shape}")
            for obj in detection:
                if obj.ndim != 1 or obj.size < 85:
                    continue  # Skip invalid detections
                
                obj = np.array(obj)
                scores = obj[5:]
                if scores.size == 0:
                    continue

                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id in selected_indices:
                    center_x = int(obj[0] * width)
                    center_y = int(obj[1] * height)
                    w = int(obj[2] * width)
                    h = int(obj[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    class_ids.append(class_id)
                    confidences.append(float(confidence))

    # Apply Non-Maximum Suppression
    if boxes:
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        if len(indices) > 0:
            indices = indices.flatten()  # Flatten to a 1D array

            for i in indices:
                box = boxes[i]
                x, y, w, h = box
                label = f"{object_names[class_ids[i]]}: {confidences[i]:.2f}"
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Convert image from BGR to RGB for displaying with matplotlib
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Display output using matplotlib
    plt.imshow(img_rgb)
    plt.axis('off')  # Hide axes
    plt.show()

# Example usage
detect_objects(image_path)
