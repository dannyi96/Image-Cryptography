from rubikencryptor.rubikencryptor import RubikCubeCrypto
from PIL import Image
from io import BytesIO
import base64
from pyscript import when, display, document

@when("click", "#transform-img-btn")
def click_handler(event):
    
    action = document.getElementById('transform-img-btn').innerText
    if action=="Encrypt":
        encrypt_image()
    elif action=="Decrypt":
        decrypt_image()
    else:
        # Invalid scenario: silently ignore
        pass

def encrypt_image():
    image_prefix, image_data = document.getElementById('input-img').src.split('base64,')
    image_bytes = base64.b64decode(image_data)
    input_image = Image.open(BytesIO(image_bytes))
    encryptor = RubikCubeCrypto(input_image)
    encrypted_image = encryptor.encrypt(alpha=8, iter_max=1)
    output_buffer = BytesIO()
    encrypted_image.save(output_buffer, format=input_image.format)
    image_bytes = output_buffer.getvalue()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    document.getElementById('output-img').src = image_prefix + 'base64,' + encoded_image
    document.getElementById('crypto-key').innerText = encryptor.encoded_key

def decrypt_image():
    image_prefix, image_data = document.getElementById('input-img').src.split('base64,')
    image_bytes = base64.b64decode(image_data)
    input_image = Image.open(BytesIO(image_bytes))
    encryptor = RubikCubeCrypto(input_image)
    keyElem = eval(document.getElementById('crypto-key').textContent)
    encrypted_image = encryptor.decrypt_with_key(keyElem)
    output_buffer = BytesIO()
    encrypted_image.save(output_buffer, format=input_image.format)
    image_bytes = output_buffer.getvalue()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    document.getElementById('output-img').src = image_prefix + 'base64,' + encoded_image
