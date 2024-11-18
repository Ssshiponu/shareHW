import os
import magic
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

ALLOWED_EXTENSIONS = {
    'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 
    'png', 'gif', 'xls', 'xlsx', 'ppt', 'pptx'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_type(file):
    # Read the first 2048 bytes to determine file type
    file_head = file.read(2048)
    file.seek(0)  # Reset file pointer
    
    mime = magic.from_buffer(file_head, mime=True)
    
    # List of allowed MIME types
    allowed_mimes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'image/jpeg',
        'image/png',
        'image/gif',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    ]
    
    return mime in allowed_mimes

def save_file(file, folder_type):
    """
    Save a file to the specified folder type (homework, notes, or id_cards)
    Returns the relative path to the saved file
    """
    if not file or not allowed_file(file.filename):
        return None
        
    if not validate_file_type(file):
        return None
    
    # Generate unique filename
    original_filename = secure_filename(file.filename)
    filename = f"{uuid.uuid4()}_{original_filename}"
    
    # Create folder if it doesn't exist
    folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_type)
    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, filename)
    file.save(file_path)
    
    # Return relative path from UPLOAD_FOLDER
    return os.path.join(folder_type, filename)

def delete_file(relative_path):
    """Delete a file given its relative path from UPLOAD_FOLDER"""
    if not relative_path:
        return False
        
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], relative_path)
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
    except Exception:
        return False
    return False
