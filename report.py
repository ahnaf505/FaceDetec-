import platform
from datetime import datetime
import random

report_standard_cache = ""

def generate_report(img1_base64, img2_base64, facenet_score, facenet_verif,
                    sface_verif, sface_score, 
                    leye1_base64, reye1_base64, nose1_base64, mouth1_base64,
                    leye2_base64, reye2_base64, nose2_base64, mouth2_base64,
                    face_contoured1, face_contoured2, img1_embeddings, img2_embeddings):
    """
    Generates a face comparison report by replacing placeholders in an HTML template with actual data.

    Args:
    img1_base64 (str): Base64 encoded string of the first image.
    img2_base64 (str): Base64 encoded string of the second image.
    facenet_score (float): Similarity score from the Facenet model.
    facenet_verif (bool): Verification result from the Facenet model.
    sface_verif (bool): Verification result from the SFace model.
    sface_score (float): Similarity score from the SFace model.
    leye1_base64 (str): Base64 encoded string of the left eye from the first image.
    reye1_base64 (str): Base64 encoded string of the right eye from the first image.
    nose1_base64 (str): Base64 encoded string of the nose from the first image.
    mouth1_base64 (str): Base64 encoded string of the mouth from the first image.
    leye2_base64 (str): Base64 encoded string of the left eye from the second image.
    reye2_base64 (str): Base64 encoded string of the right eye from the second image.
    nose2_base64 (str): Base64 encoded string of the nose from the second image.
    mouth2_base64 (str): Base64 encoded string of the mouth from the second image.
    face_contoured1 (str): Base64 encoded string of the contoured face from the first image.
    face_contoured2 (str): Base64 encoded string of the contoured face from the second image.
    img1_embeddings (list): List of embeddings from the first image.
    img2_embeddings (list): List of embeddings from the second image.
    """

    with open('report_templates/standard.html', 'r') as file:
        report_standard_cache = file.read()
        file.close()
    
    randid = random.randint(22222222, 9999999999999)

    with open('face_comparison_report - ' + str(randid) + '.html', 'w+') as file:
        img1_base64 = str(img1_base64).rstrip("'")
        img2_base64 = str(img2_base64).rstrip("'")
        report_standard_cache = report_standard_cache.replace("##base64_img1##", img1_base64.replace("b'", ""))
        report_standard_cache = report_standard_cache.replace("##base64_img2##", img2_base64.replace("b'", ""))
        report_standard_cache = report_standard_cache.replace("##facenet_score##", str(round(facenet_score, 2)))
        report_standard_cache = report_standard_cache.replace("##sface_score##", str(round(sface_score, 2)))

        if facenet_verif == True:
            report_standard_cache = report_standard_cache.replace("color_facenet", "green")
            report_standard_cache = report_standard_cache.replace("##facenet_note##", "The AI sees these two faces as the same person based on the Facenet model.")
        else:
            report_standard_cache = report_standard_cache.replace("color_facenet", "red")
            report_standard_cache = report_standard_cache.replace("##facenet_note##", "The AI sees these two faces as a different person based on the Facenet model.")

        if sface_verif == True:
            report_standard_cache = report_standard_cache.replace("color_sface", "green")
            report_standard_cache = report_standard_cache.replace("##sface_note##", "The AI sees these two faces as the same person based on the SFace model.")
        else:
            report_standard_cache = report_standard_cache.replace("color_sface", "red")
            report_standard_cache = report_standard_cache.replace("##sface_note##", "The AI sees these two faces as a different person based on the SFace model.")

        report_standard_cache = report_standard_cache.replace("##base64_img1_leye##", leye1_base64)
        report_standard_cache = report_standard_cache.replace("##base64_img1_reye##", reye1_base64)
        report_standard_cache = report_standard_cache.replace("##base64_img1_nose##", nose1_base64)
        report_standard_cache = report_standard_cache.replace("##base64_img1_mouth##", mouth1_base64)

        report_standard_cache = report_standard_cache.replace("##base64_img2_leye##", leye2_base64)
        report_standard_cache = report_standard_cache.replace("##base64_img2_reye##", reye2_base64)
        report_standard_cache = report_standard_cache.replace("##base64_img2_nose##", nose2_base64)
        report_standard_cache = report_standard_cache.replace("##base64_img2_mouth##", mouth2_base64)

        report_standard_cache = report_standard_cache.replace("##base64_img1contour##", face_contoured1)
        report_standard_cache = report_standard_cache.replace("##base64_img2contour##", face_contoured2)

        for i, embedding in enumerate(img1_embeddings):
            report_standard_cache = report_standard_cache.replace("##img1_mesh_embed_" + str(i+1) + "##", str(round(embedding, 3)))

        for i, embedding in enumerate(img2_embeddings):
            report_standard_cache = report_standard_cache.replace("##img2_mesh_embed_" + str(i+1) + "##", str(round(embedding, 3)))

        now = datetime.now()
        dnt_string = str(now.strftime("%d/%m/%Y %H:%M:%S"))

        report_standard_cache = report_standard_cache.replace("##machine##", str(platform.system() + " " + platform.release() + " " + platform.platform()))
        report_standard_cache = report_standard_cache.replace("##time_created##", dnt_string)

        file.write(report_standard_cache)
        file.close()
    
    return randid