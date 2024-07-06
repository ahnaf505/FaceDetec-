import os.path  # Importing os.path module for file path operations
import magic    # Importing python-magic library for file type detection

def is_file_exists(file_path):
    # Check if the file exists at the specified file_path
    if os.path.isfile(file_path):
        # Create a Magic instance with mime=True to get MIME type information
        mime = magic.Magic(mime=True)
        # Get the MIME type of the file at file_path
        file_mime_type = mime.from_file(file_path)
        
        # Check if the file MIME type starts with 'image/'
        if file_mime_type.startswith('image/'):
            return True  # Return True if the file is identified as an image
        else:
            return False  # Return False if the file is not identified as an image
    else:
        return None  # Return None if the file does not exist at the specified path
