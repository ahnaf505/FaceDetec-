from deepface import DeepFace
import cv2
import base64
import mediapipe as mp
from io import BytesIO
from PIL import Image

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

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
    height, width, _ = image.shape

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(image_rgb)
    if not results.multi_face_landmarks:
        return None

    landmarks = results.multi_face_landmarks[0].landmark

    left_eye_landmarks = [landmarks[i] for i in [33, 133]]
    right_eye_landmarks = [landmarks[i] for i in [362, 263]]
    nose_landmarks = [landmarks[i] for i in [1, 2, 3, 4, 5]]
    mouth_landmarks = [landmarks[i] for i in [13, 14, 78, 308]]

    def calculate_bounding_box(landmarks):
        x_coords = [int(landmark.x * width) for landmark in landmarks]
        y_coords = [int(landmark.y * height) for landmark in landmarks]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # Expand the bounding box by 20 pixels (10 pixels on each side)
        x_min = max(x_min - 10, 0)
        y_min = max(y_min - 10, 0)
        x_max = min(x_max + 10, width - 1)
        y_max = min(y_max + 10, height - 1)
        
        return x_min, y_min, x_max - x_min, y_max - y_min

    left_eye_region = calculate_bounding_box(left_eye_landmarks)
    right_eye_region = calculate_bounding_box(right_eye_landmarks)
    nose_region = calculate_bounding_box(nose_landmarks)
    mouth_region = calculate_bounding_box(mouth_landmarks)

    left_eye = image[left_eye_region[1]:left_eye_region[1]+left_eye_region[3], left_eye_region[0]:left_eye_region[0]+left_eye_region[2]]
    right_eye = image[right_eye_region[1]:right_eye_region[1]+right_eye_region[3], right_eye_region[0]:right_eye_region[0]+right_eye_region[2]]
    nose = image[nose_region[1]:nose_region[1]+nose_region[3], nose_region[0]:nose_region[0]+nose_region[2]]
    mouth = image[mouth_region[1]:mouth_region[1]+mouth_region[3], mouth_region[0]:mouth_region[0]+mouth_region[2]]

    left_eye_base64 = convert_to_base64(left_eye)
    right_eye_base64 = convert_to_base64(right_eye)
    nose_base64 = convert_to_base64(nose)
    mouth_base64 = convert_to_base64(mouth)

    return [left_eye_base64, right_eye_base64, nose_base64, mouth_base64]

def detect_and_crop_face(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Load the pre-trained Haar Cascade face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    
    # Ensure a face is detected
    if len(faces) > 0:
        # Assume only one face is detected for simplicity
        (x, y, w, h) = faces[0]
        
        # Crop the detected face region
        face_image = image[y:y+h, x:x+w]
        
        # Convert the cropped face image to base64
        _, buffer = cv2.imencode('.jpg', face_image)
        face_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return face_base64
    else:
        return None