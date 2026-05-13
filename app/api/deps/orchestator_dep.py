from fastapi import Depends

from app.api.deps.image_processing_dep import get_image_processor
from app.api.deps.ocr_processor_dep import get_ocr_processor
from app.modules.image_processing.preprocessing import ImagePreprocessor
from app.modules.ocr_processing.ocr_processor import OCRProcessor
from app.orchestator.orchestator import InvoiceOrchestator


def get_orchestator(
    image_processor: ImagePreprocessor = Depends(get_image_processor),
    ocr_processor: OCRProcessor = Depends(get_ocr_processor)
    ) -> InvoiceOrchestator:
    return InvoiceOrchestator(image_processor, ocr_processor)