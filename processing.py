from deepface import DeepFace
import cv2
import base64
import mediapipe as mp
import numpy as np
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

def run_compare(known_id_ext, unknown_id_ext):
    for i in range(50):
        try:
            facever_fn = DeepFace.verify(known_id_ext, unknown_id_ext, model_name='Facenet', distance_metric='cosine')
            facever_sf = DeepFace.verify(known_id_ext, unknown_id_ext, model_name='SFace', distance_metric='cosine')
            return [facever_fn['verified'], (1 - facever_fn['distance']) * 100, facever_sf['verified'], (1 - facever_sf['distance']) * 100]
        except ValueError as e:
            print(e)
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
    height, width, _ = image.shape
    
    # Analyze the face using DeepFace
    try:
        obj = DeepFace.analyze(image_path, actions=['emotion'], detector_backend='opencv', enforce_detection=False)
        if not obj:
            return None
    except:
        return None
    
    # Get the facial region
    facial_area = obj[0]['region']
    
    # Expand the bounding box by 10 pixels on each side
    x_min = max(facial_area['x'] - 10, 0)
    y_min = max(facial_area['y'] - 10, 0)
    x_max = min(facial_area['x'] + facial_area['w'] + 10, width - 1)
    y_max = min(facial_area['y'] + facial_area['h'] + 10, height - 1)
    
    # Crop the detected face region
    face_image = image[y_min:y_max, x_min:x_max]
    
    # Convert the cropped face image to base64
    _, buffer = cv2.imencode('.jpg', face_image)
    face_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return face_base64

def draw_skin_contour(base64_image):
    # Decode base64 to image
    image_data = base64.b64decode(base64_image)
    np_arr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Initialize mediapipe face mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

    # Convert image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get the coordinates of the landmarks
            landmarks = [(int(point.x * image.shape[1]), int(point.y * image.shape[0])) for point in face_landmarks.landmark]

            # Draw the skin contour
            skin_contour = [landmarks[i] for i in [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]]
            cv2.polylines(image, [np.array(skin_contour, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=1)

            # Draw the left eye contour
            left_eye_contour = [landmarks[i] for i in [33, 160, 158, 133, 153, 144, 163, 7, 33]]
            cv2.polylines(image, [np.array(left_eye_contour, dtype=np.int32)], isClosed=True, color=(0, 255, 255), thickness=1)

            # Draw the right eye contour
            right_eye_contour = [landmarks[i] for i in [362, 385, 387, 263, 373, 380, 388, 260, 467, 359]]
            cv2.polylines(image, [np.array(right_eye_contour, dtype=np.int32)], isClosed=True, color=(0, 255, 255), thickness=1)

            # Draw the mouth contour
            outer_lip_contour = [landmarks[i] for i in [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 61]]
            inner_lip_contour = [landmarks[i] for i in [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 78]]
            cv2.polylines(image, [np.array(outer_lip_contour, dtype=np.int32)], isClosed=True, color=(0, 0, 255), thickness=1)
            cv2.polylines(image, [np.array(inner_lip_contour, dtype=np.int32)], isClosed=True, color=(0, 0, 255), thickness=1)

            # Draw the nose contour
            nose_contour = [landmarks[i] for i in [168, 6, 197, 195, 5, 4, 1, 2, 98, 327, 168]]
            cv2.polylines(image, [np.array(nose_contour, dtype=np.int32)], isClosed=True, color=(255, 0, 0), thickness=1)

    # Convert image back to base64
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    return image_base64

def face_embeddings_extract(img_path):
    embeddings = DeepFace.represent(img_path, model_name='Facenet', detector_backend='opencv')
    return embeddings[0]['embedding']