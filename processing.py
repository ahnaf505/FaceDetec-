# Importing necessary libraries
from deepface import DeepFace  # Import DeepFace for face verification and embeddings
import cv2  # OpenCV library for image processing
import base64  # Base64 encoding for image data handling
import mediapipe as mp  # Mediapipe library for face mesh detection
import numpy as np  # NumPy for numerical operations

# Initialize mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh  # Initialize face mesh from Mediapipe
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)  # Create a FaceMesh instance for static images with single face detection

# Function to compare two images and return verification results and scores
def run_compare(known_id_ext, unknown_id_ext):
    for i in range(50):  # Try up to 50 times
        try:
            # Verify faces using Facenet model
            facever_fn = DeepFace.verify(known_id_ext, unknown_id_ext, model_name='Facenet', distance_metric='cosine')
            # Verify faces using SFace model
            facever_sf = DeepFace.verify(known_id_ext, unknown_id_ext, model_name='SFace', distance_metric='cosine')
            # Return verification results and scores
            return [facever_fn['verified'], (1 - facever_fn['distance']) * 100, facever_sf['verified'], (1 - facever_sf['distance']) * 100]
        except ValueError as e:
            pass  # Pass and try again
    return None  # Return error message after 50 attempts

# Function to convert an image to base64 encoding
def convert_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)  # Encode image to JPEG format
    image_base64 = base64.b64encode(buffer).decode('utf-8')  # Convert encoded image to base64 string
    return image_base64

# Function to cut out face features (eyes, nose, mouth) from an image
def cutout_face_features(imgpath):
    image = cv2.imread(imgpath)  # Read image using OpenCV
    height, width, _ = image.shape  # Get image dimensions

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert image to RGB format
    results = face_mesh.process(image_rgb)  # Process image to detect face mesh
    if not results.multi_face_landmarks:
        return None  # Return None if no face landmarks are detected

    landmarks = results.multi_face_landmarks[0].landmark  # Get landmarks of the first detected face

    # Define landmarks for eyes, nose, and mouth
    left_eye_landmarks = [landmarks[i] for i in [33, 133]]
    right_eye_landmarks = [landmarks[i] for i in [362, 263]]
    nose_landmarks = [landmarks[i] for i in [1, 2, 3, 4, 5]]
    mouth_landmarks = [landmarks[i] for i in [13, 14, 78, 308]]

    # Function to calculate bounding box for given landmarks
    def calculate_bounding_box(landmarks):
        x_coords = [int(landmark.x * width) for landmark in landmarks]  # Calculate x coordinates relative to image width
        y_coords = [int(landmark.y * height) for landmark in landmarks]  # Calculate y coordinates relative to image height
        x_min, x_max = min(x_coords), max(x_coords)  # Calculate minimum and maximum x coordinates
        y_min, y_max = min(y_coords), max(y_coords)  # Calculate minimum and maximum y coordinates
        
        # Expand the bounding box by 20 pixels (10 pixels on each side)
        x_min = max(x_min - 10, 0)  # Ensure x_min is within image bounds
        y_min = max(y_min - 10, 0)  # Ensure y_min is within image bounds
        x_max = min(x_max + 10, width - 1)  # Ensure x_max is within image bounds
        y_max = min(y_max + 10, height - 1)  # Ensure y_max is within image bounds
        
        return x_min, y_min, x_max - x_min, y_max - y_min  # Return adjusted bounding box dimensions

    # Calculate bounding boxes for eyes, nose, and mouth
    left_eye_region = calculate_bounding_box(left_eye_landmarks)  # Calculate bounding box for left eye landmarks
    right_eye_region = calculate_bounding_box(right_eye_landmarks)  # Calculate bounding box for right eye landmarks
    nose_region = calculate_bounding_box(nose_landmarks)  # Calculate bounding box for nose landmarks
    mouth_region = calculate_bounding_box(mouth_landmarks)  # Calculate bounding box for mouth landmarks

    # Extract and encode facial features
    left_eye = image[left_eye_region[1]:left_eye_region[1]+left_eye_region[3], left_eye_region[0]:left_eye_region[0]+left_eye_region[2]]  # Extract left eye region from image
    right_eye = image[right_eye_region[1]:right_eye_region[1]+right_eye_region[3], right_eye_region[0]:right_eye_region[0]+right_eye_region[2]]  # Extract right eye region from image
    nose = image[nose_region[1]:nose_region[1]+nose_region[3], nose_region[0]:nose_region[0]+nose_region[2]]  # Extract nose region from image
    mouth = image[mouth_region[1]:mouth_region[1]+mouth_region[3], mouth_region[0]:mouth_region[0]+mouth_region[2]]  # Extract mouth region from image

    # Convert extracted regions to base64 encoding
    left_eye_base64 = convert_to_base64(left_eye)  # Convert left eye region to base64
    right_eye_base64 = convert_to_base64(right_eye)  # Convert right eye region to base64
    nose_base64 = convert_to_base64(nose)  # Convert nose region to base64
    mouth_base64 = convert_to_base64(mouth)  # Convert mouth region to base64

    return [left_eye_base64, right_eye_base64, nose_base64, mouth_base64]  # Return list of base64 encoded features

# Function to detect and crop face from an image
def detect_and_crop_face(image_path):
    image = cv2.imread(image_path)  # Read image using OpenCV
    height, width, _ = image.shape  # Get image dimensions
    
    try:
        obj = DeepFace.analyze(image_path, actions=['emotion'], detector_backend='opencv', enforce_detection=False)  # Analyze facial features using DeepFace
        if not obj:
            return None  # Return None if no facial features are detected
    except:
        return None  # Return None if an exception occurs during analysis
    
    facial_area = obj[0]['region']  # Extract facial region from analysis results
    
    # Define expanded bounding box dimensions
    x_min = max(facial_area['x'] - 10, 0)  # Adjust x_min with a margin of 10 pixels
    y_min = max(facial_area['y'] - 10, 0)  # Adjust y_min with a margin of 10 pixels
    x_max = min(facial_area['x'] + facial_area['w'] + 10, width - 1)  # Adjust x_max with a margin of 10 pixels
    y_max = min(facial_area['y'] + facial_area['h'] + 10, height - 1)  # Adjust y_max with a margin of 10 pixels
    
    face_image = image[y_min:y_max, x_min:x_max]  # Crop face image using adjusted bounding box
    
    _, buffer = cv2.imencode('.jpg', face_image)  # Encode cropped face image to JPEG format
    face_base64 = base64.b64encode(buffer).decode('utf-8')  # Convert encoded image to base64 string
    
    return face_base64  # Return base64 encoded cropped face image

# Function to draw skin contours on a face image
def draw_skin_contour(base64_image):
    image_data = base64.b64decode(base64_image)  # Decode base64 image data
    np_arr = np.frombuffer(image_data, np.uint8)  # Convert image data to NumPy array
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # Decode image array to OpenCV format

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert image to RGB format
    results = face_mesh.process(image_rgb)  # Process image to detect face mesh

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = [(int(point.x * image.shape[1]), int(point.y * image.shape[0])) for point in face_landmarks.landmark]

            # Define and draw contours for skin, eyes, mouth, and nose
            skin_contour = [landmarks[i] for i in [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]]
            cv2.polylines(image, [np.array(skin_contour, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=1)  # Draw skin contour

            left_eye_contour = [landmarks[i] for i in [33, 160, 158, 133, 153, 144, 163, 7, 33]]
            cv2.polylines(image, [np.array(left_eye_contour, dtype=np.int32)], isClosed=True, color=(0, 255, 255), thickness=1)  # Draw left eye contour

            right_eye_contour = [landmarks[i] for i in [362, 385, 387, 263, 373, 380, 388, 260, 467, 359]]
            cv2.polylines(image, [np.array(right_eye_contour, dtype=np.int32)], isClosed=True, color=(0, 255, 255), thickness=1)  # Draw right eye contour

            outer_lip_contour = [landmarks[i] for i in [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 61]]
            inner_lip_contour = [landmarks[i] for i in [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 78]]
            cv2.polylines(image, [np.array(outer_lip_contour, dtype=np.int32)], isClosed=True, color=(0, 0, 255), thickness=1)  # Draw outer lip contour
            cv2.polylines(image, [np.array(inner_lip_contour, dtype=np.int32)], isClosed=True, color=(0, 0, 255), thickness=1)  # Draw inner lip contour

            nose_contour = [landmarks[i] for i in [168, 6, 197, 195, 5, 4, 1, 2, 98, 327, 168]]
            cv2.polylines(image, [np.array(nose_contour, dtype=np.int32)], isClosed=True, color=(255, 0, 0), thickness=1)  # Draw nose contour

    _, buffer = cv2.imencode('.jpg', image)  # Encode annotated image to JPEG format
    image_base64 = base64.b64encode(buffer).decode('utf-8')  # Convert encoded image to base64 string

    return image_base64  # Return base64 encoded annotated image

# Function to extract face embeddings from an image
def face_embeddings_extract(img_path):
    embeddings = DeepFace.represent(img_path, model_name='Facenet', detector_backend='opencv')  # Extract face embeddings using Facenet model and OpenCV detector
    return embeddings[0]['embedding']  # Return embeddings of the first face detected
