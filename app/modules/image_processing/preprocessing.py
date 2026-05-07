import cv2
import numpy as np

class ImagePrepocessor:
    
    def __init__(self):
        pass
    
    def preprocess_image(self, image):
        
        resized = self._resize(image)
        in_grayscale = self._to_grayscale(resized)
        shadows_removed = self._eliminate_shadows(in_grayscale)
        deskewed = self._deskow(shadows_removed)
        binarized = self._binarization(deskewed)
        denoised = self._denoise(binarized)
        return denoised
        
    
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
        
        # Detectar bordes
        edges = cv2.Canny(image, 50, 150, apertureSize=3)

        # Detectar líneas rectas en los bordes
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi / 180,
            threshold=100,
            minLineLength=100,
            maxLineGap=10
        )

        if lines is None:
            return image 

        # Calcular el ángulo promedio de todas las líneas detectadas
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 != x1:  # Evitar división por cero
                angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
                if abs(angle) < 45:
                    angles.append(angle)

        if not angles:
            return image

        median_angle = np.median(angles)

        if abs(median_angle) < 0.5:
            return image

        h, w = image.shape
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        rotated = cv2.warpAffine(
            image, rotation_matrix, (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE     
        )
        
        return rotated
    
    def _binarization(self, image):
        return cv2.adaptiveThreshold(
            image, 
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=21,
            C=5
        )
    
    def _denoise(self, image):
        return cv2.fastNlMeansDenoising(image, h=10)
