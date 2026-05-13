
from fastapi import Request

from app.modules.ocr_processing.ocr_processor import OCRProcessor


def get_ocr_processor(request: Request) -> OCRProcessor:
    return OCRProcessor(reader=request.app.state.ocr_reader)