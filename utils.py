from base64 import b64decode
from PIL import Image
from io import BytesIO

def decodificar_imagen_base64(img: str):
    data: str = img.split(',')[1]
    binario: bytes = b64decode(data)
    imagen: Image = Image.open(BytesIO(binario))
    return imagen