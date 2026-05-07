from app.modules.image_processing.preprocessing import ImagePrepocessor


def get_image_processor() -> ImagePrepocessor:
    return ImagePrepocessor()