from app.modules.image_processing.preprocessing import ImagePreprocessor


def get_image_processor() -> ImagePreprocessor:
    return ImagePreprocessor()