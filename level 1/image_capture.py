# image_capture.py
import cv2

class ImageCapture:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
    
    def capture_image(self, section):
        ret, frame = self.camera.read()
        if ret:
            image_file = f"{section}_image.jpg"
            cv2.imwrite(image_file, frame)
            print(f"Image captured for {section} and saved as {image_file}")
        else:
            print("Failed to capture image.")
    
    def __del__(self):
        self.camera.release()
