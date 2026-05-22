from fastapi import Depends

from app.api.deps.image_processing_dep import get_image_processor
from app.api.deps.llm_extractor_dep import get_llm_extractor
from app.api.deps.ocr_processor_dep import get_ocr_processor
from app.modules.image_processing.preprocessing import ImagePreprocessor
from app.modules.llm_extractor.llm_extractor import LLMExtractor
from app.modules.ocr_processing.ocr_processor import OCRProcessor
from app.orchestator.orchestator import InvoiceOrchestator


def get_orchestator(
    image_processor: ImagePreprocessor = Depends(get_image_processor),
    ocr_processor: OCRProcessor = Depends(get_ocr_processor),
    llm_extractor: LLMExtractor = Depends(get_llm_extractor)
    ) -> InvoiceOrchestator:
    return InvoiceOrchestator(image_processor, ocr_processor, llm_extractor)