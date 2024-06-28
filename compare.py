from deepface import DeepFace

def run_compare(known_id_ext, unknown_id_ext):
    try:
        facever = DeepFace.verify(known_id_ext, unknown_id_ext, model_name='Facenet')
        return [facever['verified'], facever['distance']]
    except ValueError:
        return "err1"
    
