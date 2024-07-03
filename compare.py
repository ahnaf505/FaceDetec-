from deepface import DeepFace
import cv2
import base64
from io import BytesIO

def run_compare(known_id_ext, unknown_id_ext):
    for i in range(100):
        try:
            facever = DeepFace.verify(known_id_ext, unknown_id_ext, model_name='Facenet', distance_metric='cosine')
            return [facever['verified'], (1 - facever['distance']) * 100]
        except ValueError:
            pass
    return "err1"

def convert_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return image_base64

def cutout_face_features(imgpath):
    img_path = "path_to_image.jpg"
    image = cv2.imread(img_path)

    obj = DeepFace.analyze(img_path, actions=['emotion'], detector_backend='opencv', enforce_detection=False)

    # Get the facial landmarks
    facial_area = obj['region']

    # Define regions for the left eye, right eye, nose, and mouth
    # These values are approximate and may need adjustment based on the landmark positions.
    left_eye_region = (facial_area['x'], facial_area['y'], facial_area['w']//3, facial_area['h']//4)
    right_eye_region = (facial_area['x'] + 2 * facial_area['w']//3, facial_area['y'], facial_area['w']//3, facial_area['h']//4)
    nose_region = (facial_area['x'] + facial_area['w']//3, facial_area['y'] + facial_area['h']//4, facial_area['w']//3, facial_area['h']//3)
    mouth_region = (facial_area['x'] + facial_area['w']//4, facial_area['y'] + 3 * facial_area['h']//4, facial_area['w']//2, facial_area['h']//4)

    # Crop the regions
    left_eye = image[left_eye_region[1]:left_eye_region[1]+left_eye_region[3], left_eye_region[0]:left_eye_region[0]+left_eye_region[2]]
    right_eye = image[right_eye_region[1]:right_eye_region[1]+right_eye_region[3], right_eye_region[0]:right_eye_region[0]+right_eye_region[2]]
    nose = image[nose_region[1]:nose_region[1]+nose_region[3], nose_region[0]:nose_region[0]+nose_region[2]]
    mouth = image[mouth_region[1]:mouth_region[1]+mouth_region[3], mouth_region[0]:mouth_region[0]+mouth_region[2]]

    # Convert cropped images to base64
    left_eye_base64 = convert_to_base64(left_eye)
    right_eye_base64 = convert_to_base64(right_eye)
    nose_base64 = convert_to_base64(nose)
    mouth_base64 = convert_to_base64(mouth)