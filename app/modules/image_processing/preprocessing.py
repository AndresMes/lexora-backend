import cv2
import numpy as np


class ImagePreprocessor:

    def preprocess_image(self, image_bytes: bytes) -> bytes:

        image = self._bytes_to_image(image_bytes)

        # cropped = self._crop_document(image)  # descomentar cuando esté listo

        resized = self._resize(image)
        grayscale = self._to_grayscale(resized)
        denoised = self._denoise(grayscale)
        shadow_free = self._eliminate_shadows(denoised)
        sharpened = self._sharpen(shadow_free)
        deskewed = self._deskew(sharpened)

        return self._image_to_bytes(deskewed)

    def _bytes_to_image(self, image_bytes: bytes) -> np.ndarray:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("No se pudo decodificar la imagen")
        return img

    def _image_to_bytes(self, image: np.ndarray) -> bytes:
        success, buffer = cv2.imencode('.png', image)
        if not success:
            raise ValueError("No se pudo codificar la imagen")
        return buffer.tobytes()

    def _resize(self, image: np.ndarray) -> np.ndarray:
        h, w = image.shape[:2]
        target_width = 1800
        if w >= target_width:
            return image
        ratio = target_width / w
        return cv2.resize(
            image,
            (target_width, int(h * ratio)),
            interpolation=cv2.INTER_CUBIC
        )

    def _to_grayscale(self, image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def _eliminate_shadows(self, image: np.ndarray) -> np.ndarray:
        dilated = cv2.dilate(image, np.ones((7, 7), np.uint8))
        background = cv2.medianBlur(dilated, 21)
        diff = cv2.absdiff(image, background)
        result = 255 - diff
        return cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX)

    def _denoise(self, image: np.ndarray) -> np.ndarray:
        return cv2.fastNlMeansDenoising(image, h=7)

    def _sharpen(self, image: np.ndarray) -> np.ndarray:
        kernel = np.array([
            [0, -1,  0],
            [-1,  5, -1],
            [0, -1,  0]
        ])
        return cv2.filter2D(image, -1, kernel)

    def _deskew(self, image: np.ndarray) -> np.ndarray:
        coords = np.column_stack(np.where(image > 0))
        if len(coords) == 0:
            return image
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        if abs(angle) < 0.5:
            return image
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(
            image, matrix, (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )

    def _crop_document(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(
            blur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            21, 10
        )
        kernel = np.ones((5, 5), np.uint8)
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return image
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        padding = 20
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + padding * 2)
        h = min(image.shape[0] - y, h + padding * 2)
        return image[y:y+h, x:x+w]