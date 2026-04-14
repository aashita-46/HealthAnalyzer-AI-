import easyocr
import numpy as np

class OCRReader:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def read_text(self, pil_image):
        img_array = np.array(pil_image)
        results = self.reader.readtext(img_array)
        text = " ".join([res[1] for res in results])
        return text.strip() if text else "Generic Product"