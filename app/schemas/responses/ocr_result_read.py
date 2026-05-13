from pydantic import BaseModel

from app.schemas.responses.ocr_detection_read import OCRDetection


class OCRResult(BaseModel):
    raw_text: str
    document_confidence: float
    detections: list[OCRDetection]