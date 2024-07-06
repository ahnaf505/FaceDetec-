# Importing necessary libraries
from deepface import DeepFace
import cv2
import base64
import mediapipe as mp
import numpy as np

# Utility function to convert an image to base64 encoding
def convert_to_base64(image):
    """
    Converts an OpenCV image (BGR format) to base64 encoding.

    Args:
    - image (numpy.ndarray): Input image in OpenCV format (BGR).

    Returns:
    - str: Base64 encoded string of the image.
    """
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return image_base64

# Function to compare two images and return verification results and scores
def run_compare(known_id_ext, unknown_id_ext):
    """
    Compares two images using Facenet and SFace models for face verification.

    Args:
    - known_id_ext (str): File path or base64 encoded string of the known image.
    - unknown_id_ext (str): File path or base64 encoded string of the unknown image.

    Returns:
    - list or None: List containing verification results and confidence scores:
      [facever_fn['verified'], (1 - facever_fn['distance']) * 100,
       facever_sf['verified'], (1 - facever_sf['distance']) * 100]
      Returns None if verification fails after 10 attempts.
    """
    for i in range(10):  # Reduced number of attempts to 10
        try:
            # Verify faces using Facenet model
            facever_fn = DeepFace.verify(known_id_ext, unknown_id_ext, model_name='Facenet', distance_metric='cosine')
            # Verify faces using SFace model
            facever_sf = DeepFace.verify(known_id_ext, unknown_id_ext, model_name='SFace', distance_metric='cosine')
            # Return verification results and scores
            return [facever_fn['verified'], (1 - facever_fn['distance']) * 100, facever_sf['verified'], (1 - facever_sf['distance']) * 100]
        except ValueError:
            pass
    return None  # Return None after 10 attempts

# Function to cut out face features (eyes, nose, mouth) from an image
def cutout_face_features(imgpath):
    """
    Detects and cuts out specific facial features (eyes, nose, mouth) from an image.

    Args:
    - imgpath (str): File path of the input image.

    Returns:
    - list or None: List containing base64 encoded strings of:
      [left_eye_base64, right_eye_base64, nose_base64, mouth_base64]
      Returns None if no face landmarks are detected.
    """
    # Initialize mediapipe face mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

    image = cv2.imread(imgpath)
    height, width, _ = image.shape

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    if not results.multi_face_landmarks:
        return None

    landmarks = results.multi_face_landmarks[0].landmark

    # Define landmarks for eyes, nose, and mouth
    left_eye_landmarks = [landmarks[i] for i in [33, 133]]
    right_eye_landmarks = [landmarks[i] for i in [362, 263]]
    nose_landmarks = [landmarks[i] for i in [1, 2, 3, 4, 5]]
    mouth_landmarks = [landmarks[i] for i in [13, 14, 78, 308]]

    # Function to calculate bounding box for given landmarks
    def calculate_bounding_box(landmarks, expand_percent=0.05):
        x_coords = [int(landmark.x * width) for landmark in landmarks]
        y_coords = [int(landmark.y * height) for landmark in landmarks]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # Expand the bounding box by a percentage
        expand_x = int((x_max - x_min) * expand_percent)
        expand_y = int((y_max - y_min) * expand_percent)
        
        x_min = max(x_min - expand_x, 0)
        y_min = max(y_min - expand_y, 0)
        x_max = min(x_max + expand_x, width - 1)
        y_max = min(y_max + expand_y, height - 1)
        
        return x_min, y_min, x_max - x_min, y_max - y_min

    # Calculate bounding boxes for eyes, nose, and mouth
    left_eye_region = calculate_bounding_box(left_eye_landmarks)
    right_eye_region = calculate_bounding_box(right_eye_landmarks)
    nose_region = calculate_bounding_box(nose_landmarks)
    mouth_region = calculate_bounding_box(mouth_landmarks)

    # Extract and encode facial features
    left_eye = image[left_eye_region[1]:left_eye_region[1]+left_eye_region[3], left_eye_region[0]:left_eye_region[0]+left_eye_region[2]]
    right_eye = image[right_eye_region[1]:right_eye_region[1]+right_eye_region[3], right_eye_region[0]:right_eye_region[0]+right_eye_region[2]]
    nose = image[nose_region[1]:nose_region[1]+nose_region[3], nose_region[0]:nose_region[0]+nose_region[2]]
    mouth = image[mouth_region[1]:mouth_region[1]+mouth_region[3], mouth_region[0]:mouth_region[0]+mouth_region[2]]

    left_eye_base64 = convert_to_base64(left_eye)
    right_eye_base64 = convert_to_base64(right_eye)
    nose_base64 = convert_to_base64(nose)
    mouth_base64 = convert_to_base64(mouth)

    return [left_eye_base64, right_eye_base64, nose_base64, mouth_base64]

# Function to detect and crop face from an image
def detect_and_crop_face(image_path):
    """
    Detects and crops the face from an image.

    Args:
    - image_path (str): File path of the input image.

    Returns:
    - str or None: Base64 encoded string of the cropped face image.
      Returns None if face detection fails.
    """
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    
    try:
        obj = DeepFace.analyze(image_path, actions=['emotion'], detector_backend='opencv', enforce_detection=False)
        if not obj:
            return None
    except Exception:
        return None
    
    facial_area = obj[0]['region']
    
    expand_percent = 0.05  # Expand the bounding box by 5%
    x_min = max(int(facial_area['x'] - facial_area['w'] * expand_percent), 0)
    y_min = max(int(facial_area['y'] - facial_area['h'] * expand_percent), 0)
    x_max = min(int(facial_area['x'] + facial_area['w'] * (1 + expand_percent)), width - 1)
    y_max = min(int(facial_area['y'] + facial_area['h'] * (1 + expand_percent)), height - 1)
    
    face_image = image[y_min:y_max, x_min:x_max]
    face_base64 = convert_to_base64(face_image)
    
    return face_base64

# Function to draw skin contours on a face image
def draw_skin_contour(base64_image):
    """
    Draws skin, eyes, mouth, and nose contours on a face image.

    Args:
    - base64_image (str): Base64 encoded string of the input image.

    Returns:
    - str: Base64 encoded string of the image with drawn contours.
    """
    image_data = base64.b64decode(base64_image)
    np_arr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = [(int(point.x * image.shape[1]), int(point.y * image.shape[0])) for point in face_landmarks.landmark]

            # Define and draw contours for skin, eyes, mouth, and nose
            skin_contour = [landmarks[i] for i in [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]]
            cv2.polylines(image, [np.array(skin_contour, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=1)

            left_eye_contour = [landmarks[i] for i in [33, 160, 158, 133, 153, 144, 163, 7, 33]]
            cv2.polylines(image, [np.array(left_eye_contour, dtype=np.int32)], isClosed=True, color=(0, 255, 255), thickness=1)

            right_eye_contour = [landmarks[i] for i in [362, 385, 387, 263, 373, 380, 388, 260, 467, 359]]
            cv2.polylines(image, [np.array(right_eye_contour, dtype=np.int32)], isClosed=True, color=(0, 255, 255), thickness=1)

            outer_lip_contour = [landmarks[i] for i in [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 61]]
            inner_lip_contour = [landmarks[i] for i in [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 78]]
            cv2.polylines(image, [np.array(outer_lip_contour, dtype=np.int32)], isClosed=True, color=(0, 0, 255), thickness=1)
            cv2.polylines(image, [np.array(inner_lip_contour, dtype=np.int32)], isClosed=True, color=(0, 0, 255), thickness=1)

            nose_contour = [landmarks[i] for i in [168, 6, 197, 195, 5, 4, 1, 2, 98, 327, 168]]
            cv2.polylines(image, [np.array(nose_contour, dtype=np.int32)], isClosed=True, color=(255, 0, 0), thickness=1)

    image_base64 = convert_to_base64(image)

    return image_base64

# Function to extract face embeddings from an image
def face_embeddings_extract(img_path):
    """
    Extracts face embeddings (vector representations) from an image using the Facenet model.

    Args:
    - img_path (str): File path of the input image.

    Returns:
    - numpy.ndarray: Numeric vector (embedding) representing the face.
    """
    embeddings = DeepFace.represent(img_path, model_name='Facenet', detector_backend='opencv')
    return embeddings[0]['embedding']
