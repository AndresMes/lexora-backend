from app.modules.image_processing.preprocessing import ImagePrepocessor


class InvoiceOrchestator:
    
    def __init__(self, preprocessor: ImagePrepocessor):
        self.preprocessor = preprocessor
        
    async def process_invoice(self, file_bytes: bytes, filename: str):
        
        processed_image = self.preprocessor.preprocess_image(file_bytes)
        