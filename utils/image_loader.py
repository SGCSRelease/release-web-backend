import os, base64
from release_web_backend.settings import BASE_DIR

IMAGE_DIR = os.path.join(BASE_DIR, 'database')

def load_image(path: str) -> str:
    image_path = os.path.join(IMAGE_DIR, path)
    if not os.path.exists(image_path):
        return ''
    
    image_file = open(image_path, 'rb')
    return base64.b64encode(image_file.read()).decode('utf-8')

def save_image(path: str, image: str) -> None:
    image_path = os.path.join(IMAGE_DIR, path)

    image_file = open(image_path, 'wb')
    image_file.write(base64.b64decode(image))