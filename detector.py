import cv2
from ultralytics import YOLO
from PIL import Image

class ShelfDetector:
    def __init__(self):
        # Uses pre-trained weights to ensure boxes are found
        self.model = YOLO('yolov8n.pt') 

    def detect(self, image_path):
        img = cv2.imread(image_path)
        if img is None: return []
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Detect common objects
        results = self.model(img_rgb, conf=0.2)
        detections = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                crop = Image.fromarray(img_rgb[y1:y2, x1:x2])
                detections.append({
                    "bbox": [x1, y1, x2, y2], 
                    "crop": crop
                })

        # Fallback grid if YOLO is unsure
        if not detections:
            h, w, _ = img_rgb.shape
            for i in range(2):
                for j in range(3):
                    x1, y1, x2, y2 = j*w//3, i*h//2, (j+1)*w//3, (i+1)*h//2
                    crop = Image.fromarray(img_rgb[y1:y2, x1:x2])
                    detections.append({"bbox": [x1, y1, x2, y2], "crop": crop})
        return detections