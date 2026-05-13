from pydantic import BaseModel


class OCRDetection(BaseModel):
    text: str
    confidence: float
    bbox: list[list[int]]