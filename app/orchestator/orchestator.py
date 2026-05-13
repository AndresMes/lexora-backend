from app.modules.image_processing.preprocessing import ImagePreprocessor
from app.modules.ocr_processing.ocr_processor import OCRProcessor


class InvoiceOrchestator:
    
    def __init__(self, preprocessor: ImagePreprocessor, ocr_processor: OCRProcessor):
        self.preprocessor = preprocessor
        self.ocr_processor = ocr_processor
        
    async def process_invoice(self, file_bytes: bytes, filename: str):
        
        processed_image = self.preprocessor.preprocess_image(file_bytes)
        text = self.ocr_processor.extract_text(processed_image)
        