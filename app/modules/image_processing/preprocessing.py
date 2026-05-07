import cv2
import numpy as np

class ImagePrepocessor:
    
    def __init__(self):
        pass
    
    def preprocess_image(self):
        pass
    
    def _resize(self, image):
        
        h, w = image.shape[:2]
        
        if(w <= 1200):
            return image
        
        ratio = 1200 / w
        
        image_resized = cv2.resize(image, (1200, int(ratio * h)), interpolation=cv2.INTER_AREA)
        
        return image_resized
    
    def _to_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def _eliminate_shadows(self, image):
        dilatated_image = cv2.dilate(image, np.ones((7,7), np.uint8))
        blur_image = cv2.medianBlur(dilatated_image, 21)
        diff = cv2.absdiff(image, blur_image)
        result = 255 - diff
        return cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX)
        
    
    def _deskow(self, image):
        pass
    
    def _binarization(self, image):
        pass
    
    def _denoise(self, image):
        pass