import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def save_file(file, folder):
    """
    Save uploaded file to the specified folder with a secure filename.
    Returns the relative path to the saved file.
    """
    if not file:
        return None
        
    if not allowed_file(file.filename):
        return None
    
    # Create a secure filename with UUID to prevent collisions
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    
    # Ensure upload folder exists
    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(upload_folder, unique_filename)
    try:
        file.save(file_path)
        return os.path.join(folder, unique_filename)
    except Exception as e:
        current_app.logger.error(f"Error saving file: {str(e)}")
        if os.path.exists(file_path):
            os.remove(file_path)
        return None

def delete_file(file_path):
    """Delete a file from the upload folder."""
    if not file_path:
        return
        
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
    except Exception as e:
        current_app.logger.error(f"Error deleting file: {str(e)}")
