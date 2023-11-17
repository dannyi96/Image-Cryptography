from rubikencryptor.rubikencryptor import RubikCubeCrypto
from PIL import Image
from io import BytesIO
import base64
from pyscript import when, display, document

@when("click", "#transform-image")
def click_handler(event):
    image_prefix, image_data = document.getElementById('input-image').src.split('base64,')
    image_bytes = base64.b64decode(image_data)
    input_image = Image.open(BytesIO(image_bytes))
    encryptor = RubikCubeCrypto(input_image)
    encrypted_image = encryptor.encrypt(alpha=8, iter_max=1)
    output_buffer = BytesIO()
    encrypted_image.save(output_buffer, format=input_image.format)
    image_bytes = output_buffer.getvalue()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    document.getElementById('output-image').src = image_prefix + 'base64,' + encoded_image
    document.getElementById('encoded-key').innerText = encryptor.encoded_key
    