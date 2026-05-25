from uuid import uuid4

import cloudinary.uploader
import io

def upload_file(file_bytes: bytes) -> str:
    cloudinary_asset_id = str(uuid4())
    result = cloudinary.uploader.upload(
        io.BytesIO(file_bytes),
        public_id=cloudinary_asset_id,
        resource_type="auto"
    )
    return result["secure_url"]