from deepface import DeepFace
import cv2
import base64
from io import BytesIO

def run_compare(known_id_ext, unknown_id_ext):
    for i in range(50):
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
    image = cv2.imread(imgpath)

    obj = DeepFace.analyze(imgpath, actions=['emotion'], detector_backend='opencv', enforce_detection=False)
    print(obj[0])
    facial_area = obj[0]['region']

    left_eye_region = (facial_area['x'], facial_area['y'], facial_area['w']//3, facial_area['h']//4)
    right_eye_region = (facial_area['x'] + 2 * facial_area['w']//3, facial_area['y'], facial_area['w']//3, facial_area['h']//4)
    nose_region = (facial_area['x'] + facial_area['w']//3, facial_area['y'] + facial_area['h']//4, facial_area['w']//3, facial_area['h']//3)
    mouth_region = (facial_area['x'] + facial_area['w']//4, facial_area['y'] + 3 * facial_area['h']//4, facial_area['w']//2, facial_area['h']//4)

    left_eye = image[left_eye_region[1]:left_eye_region[1]+left_eye_region[3], left_eye_region[0]:left_eye_region[0]+left_eye_region[2]]
    right_eye = image[right_eye_region[1]:right_eye_region[1]+right_eye_region[3], right_eye_region[0]:right_eye_region[0]+right_eye_region[2]]
    nose = image[nose_region[1]:nose_region[1]+nose_region[3], nose_region[0]:nose_region[0]+nose_region[2]]
    mouth = image[mouth_region[1]:mouth_region[1]+mouth_region[3], mouth_region[0]:mouth_region[0]+mouth_region[2]]

    left_eye_base64 = convert_to_base64(left_eye)
    right_eye_base64 = convert_to_base64(right_eye)
    nose_base64 = convert_to_base64(nose)
    mouth_base64 = convert_to_base64(mouth)
    
    return [left_eye_base64, right_eye_base64, nose_base64, mouth_base64]