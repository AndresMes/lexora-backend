import cv2
import numpy as np

from app.schemas.responses.ocr_detection_read import OCRDetection
from app.schemas.responses.ocr_result_read import OCRResult

class OCRProcessor:
    
    def __init__(self, reader):
        self.reader = reader
    
    def extract_text(self, image_bytes: bytes) -> OCRResult:
        
        image = self._bytes_to_image(image_bytes)
        
        results = self.reader.readtext(
            image,
            detail=1,
            paragraph=False,
            width_ths=0.7,
            height_ths=0.7,
            decoder='greedy',
            text_threshold=0.7,
            low_text=0.3,
            link_threshold=0.4
        )

        extracted: list[OCRDetection] = []

        for result in results:
            bbox, text, confidence = result
            if confidence > 0.4:
                
                clean_bbox = [
                    [int(point[0]), int(point[1])]
                    for point in bbox
                ]
                
                extracted.append(
                    OCRDetection(
                        text=text,
                        confidence=round(float(confidence),4),
                        bbox=clean_bbox
                    )
                )

        rows = self._reconstruct_rows(extracted)
        
        avg_confidence = np.mean([
            e.confidence
            for e in extracted
        ]) if extracted else 0.0
        
        return OCRResult(
            raw_text="\n".join(rows),
            document_confidence=round(float(avg_confidence), 4),
            detections=extracted
        )

    
    def _reconstruct_rows(self, extracted:list[OCRDetection], y_tolerance: int = 20) -> list:
        groups = []

        for element in extracted:
            y1 = element.bbox[0][1]
            placed = False

            for group in groups:
                
                group_y = np.mean([
                    e.bbox[0][1]
                    for e in group
                ])
                
                if abs(y1 - group_y) <= y_tolerance:
                    group.append(element)
                    placed = True
                    break

            if not placed:
                groups.append([element])

        rows = []
        for group in groups:
            sorted_group = sorted(
                group,
                key=lambda e: e.bbox[0][0]
            )

            row_text = " | ".join([
                e.text
                for e in sorted_group
            ])
            
            rows.append(row_text)

        return rows
    
    def _bytes_to_image(self, image_bytes: bytes) -> np.ndarray:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("No se pudo decodificar la imagen")
        return img