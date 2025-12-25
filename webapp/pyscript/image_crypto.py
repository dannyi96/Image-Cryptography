from rubikencryptor.rubikencryptor import RubikCubeCrypto
from PIL import Image
from io import BytesIO
import base64
import time
import traceback
from pyscript import when, display, document

def show_status(message, msg_type='info'):
    """Show status message using JavaScript function"""
    from js import showStatus
    showStatus(message, msg_type)

def show_loading(text='Processing image...'):
    """Show loading overlay"""
    from js import showLoading
    showLoading(text)

def hide_loading():
    """Hide loading overlay"""
    from js import hideLoading
    hideLoading()

def update_progress(percent):
    """Update progress bar"""
    from js import updateProgress
    updateProgress(percent)

def validate_inputs():
    """Validate user inputs"""
    from js import validateInputs
    return validateInputs()

def get_current_mode():
    """Get current mode (encrypt/decrypt)"""
    from js import currentMode
    return currentMode()

def update_performance_info(process_time):
    """Update performance information display"""
    document.getElementById('process-time').textContent = f"{process_time:.0f}"
    document.getElementById('performance-info').style.display = 'block'

def get_image_from_element(element_id):
    """Extract image data from DOM element"""
    try:
        img_src = document.getElementById(element_id).src
        if 'placeholder' in img_src:
            raise ValueError("No image loaded")
        
        image_prefix, image_data = img_src.split('base64,')
        image_bytes = base64.b64decode(image_data)
        return Image.open(BytesIO(image_bytes))
    except Exception as e:
        raise ValueError(f"Failed to load image: {str(e)}")

def set_output_image(image, original_format='PNG'):
    """Set the output image in the DOM"""
    try:
        output_buffer = BytesIO()
        # Ensure we save in a web-compatible format
        save_format = 'PNG' if original_format.upper() not in ['PNG', 'JPEG', 'JPG'] else original_format.upper()
        if save_format == 'JPG':
            save_format = 'JPEG'
            
        image.save(output_buffer, format=save_format)
        image_bytes = output_buffer.getvalue()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Set the image source
        document.getElementById('output-img').src = f"data:image/{save_format.lower()};base64,{encoded_image}"
        
        # Show download section
        document.getElementById('download-section').style.display = 'flex'
        
        return True
    except Exception as e:
        show_status(f"Failed to set output image: {str(e)}", 'error')
        return False

@when("click", "#transform-img-btn")
def click_handler(event):
    """Handle encrypt/decrypt button click"""
    try:
        # Validate inputs first
        if not validate_inputs():
            return
            
        mode = get_current_mode()
        
        if mode == "encrypt":
            encrypt_image()
        elif mode == "decrypt":
            decrypt_image()
        else:
            show_status("Invalid operation mode", 'error')
            
    except Exception as e:
        hide_loading()
        show_status(f"Operation failed: {str(e)}", 'error')
        print(f"Error in click_handler: {traceback.format_exc()}")

def encrypt_image():
    """Perform image encryption with progress tracking"""
    start_time = time.time()
    
    try:
        show_loading("Loading image...")
        update_progress(10)
        
        # Get input image
        input_image = get_image_from_element('input-img')
        original_format = input_image.format or 'PNG'
        
        show_loading("Initializing encryption...")
        update_progress(20)
        
        # Get parameters
        alpha = int(document.getElementById('alpha-input').value)
        iter_max = int(document.getElementById('iter-input').value)
        
        show_loading("Creating encryption keys...")
        update_progress(30)
        
        # Create encryptor
        encryptor = RubikCubeCrypto(input_image)
        
        show_loading("Encrypting image...")
        update_progress(50)
        
        # Perform encryption (without saving key file)
        encryptor.create_key(alpha, iter_max)
        
        # Manual encryption process with progress updates
        for i in range(iter_max):
            progress = 50 + (40 * (i + 1) / iter_max)
            update_progress(progress)
            show_loading(f"Encryption iteration {i + 1}/{iter_max}...")
            
            encryptor.roll_row(encrypt_flag=True)
            encryptor.roll_column(encrypt_flag=True)
            encryptor.xor_pixels()
        
        show_loading("Finalizing...")
        update_progress(95)
        
        # Create output image
        encrypted_image = Image.fromarray(encryptor.new_rgb_array.astype('uint8'))
        
        # Set output image
        if set_output_image(encrypted_image, original_format):
            # Store the key
            document.getElementById('crypto-key').textContent = encryptor.encoded_key.decode('utf-8')
            
            update_progress(100)
            
            # Calculate and display performance
            process_time = (time.time() - start_time) * 1000
            update_performance_info(process_time)
            
            hide_loading()
            show_status(f"Image encrypted successfully in {process_time:.0f}ms", 'success')
        else:
            raise Exception("Failed to set output image")
            
    except Exception as e:
        hide_loading()
        show_status(f"Encryption failed: {str(e)}", 'error')
        print(f"Encryption error: {traceback.format_exc()}")

def decrypt_image():
    """Perform image decryption with progress tracking"""
    start_time = time.time()
    
    try:
        show_loading("Loading encrypted image...")
        update_progress(10)
        
        # Get encrypted image
        input_image = get_image_from_element('input-img')
        original_format = input_image.format or 'PNG'
        
        show_loading("Loading decryption key...")
        update_progress(20)
        
        # Get key
        key_content = document.getElementById('crypto-key').textContent.strip()
        if not key_content:
            raise ValueError("No decryption key provided")
        
        show_loading("Initializing decryption...")
        update_progress(30)
        
        # Create decryptor
        decryptor = RubikCubeCrypto(input_image)
        
        show_loading("Loading key parameters...")
        update_progress(40)
        
        # Load key
        decryptor.load_key(key_content.encode('utf-8'))
        
        show_loading("Decrypting image...")
        update_progress(50)
        
        # Manual decryption process with progress updates
        for i in range(decryptor.iter_max):
            progress = 50 + (40 * (i + 1) / decryptor.iter_max)
            update_progress(progress)
            show_loading(f"Decryption iteration {i + 1}/{decryptor.iter_max}...")
            
            decryptor.xor_pixels()
            decryptor.roll_column(encrypt_flag=False)
            decryptor.roll_row(encrypt_flag=False)
        
        show_loading("Finalizing...")
        update_progress(95)
        
        # Create output image
        decrypted_image = Image.fromarray(decryptor.new_rgb_array.astype('uint8'))
        
        # Set output image
        if set_output_image(decrypted_image, original_format):
            update_progress(100)
            
            # Calculate and display performance
            process_time = (time.time() - start_time) * 1000
            update_performance_info(process_time)
            
            hide_loading()
            show_status(f"Image decrypted successfully in {process_time:.0f}ms", 'success')
        else:
            raise Exception("Failed to set output image")
            
    except Exception as e:
        hide_loading()
        show_status(f"Decryption failed: {str(e)}", 'error')
        print(f"Decryption error: {traceback.format_exc()}")

# Initialize PyScript
def initialize():
    """Initialize the application"""
    try:
        show_status("Application ready", 'success')
        print("PyScript initialized successfully")
    except Exception as e:
        print(f"Initialization error: {traceback.format_exc()}")

# Run initialization
initialize()
