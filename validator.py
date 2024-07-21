from PIL import Image, UnidentifiedImageError
import base64
from io import BytesIO

def is_base64_image(base64_string: str) -> bool:
        try:
            image_data = base64.b64decode(base64_string)
            image = Image.open(BytesIO(image_data))
            image.verify()  # This verifies that an image is valid
            return True
        except (base64.binascii.Error, UnidentifiedImageError):
            return False
