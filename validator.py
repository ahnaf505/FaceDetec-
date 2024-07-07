import os.path
import magic

def is_file_exists(file_path):
    if os.path.isfile(file_path):
        mime = magic.Magic(mime=True)
        file_mime_type = mime.from_file(file_path)

        if file_mime_type.startswith('image/'):
            return True
        else:
            return False
    else:
        return None
