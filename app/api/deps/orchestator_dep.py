from fastapi import Depends

from app.api.deps.image_processing_dep import get_image_processor
from app.modules.image_processing.preprocessing import ImagePrepocessor
from app.orchestator.orchestator import InvoiceOrchestator


def get_orchestator(
    image_processor: ImagePrepocessor = Depends(get_image_processor)
    ) -> InvoiceOrchestator:
    return InvoiceOrchestator(image_processor)