from app.modules.image_processing.preprocessing import ImagePreprocessor
from app.modules.llm_extractor.llm_extractor import LLMExtractor
from app.modules.ocr_processing.ocr_processor import OCRProcessor


class InvoiceOrchestator:
    
    def __init__(self, preprocessor: ImagePreprocessor, ocr_processor: OCRProcessor, llm_extractor: LLMExtractor):
        self.preprocessor = preprocessor
        self.ocr_processor = ocr_processor
        self.llm_extractor = llm_extractor
        
    async def process_invoice(self, file_bytes: bytes):
        
        processed_image = self.preprocessor.preprocess_image(file_bytes)
        ocr_result = self.ocr_processor.extract_text(processed_image)
        extracted_data = self.llm_extractor.extract_invoice_data(ocr_result)
        return extracted_data
        