

report_standard_cache = ""

def generate_report(img1_base64, img2_base64, facenet_score, facenet_verif,
                    sface_verif, sface_score, 
                    leye1_base64, reye1_base64, nose1_base64, mouth1_base64,
                    leye2_base64, reye2_base64, nose2_base64, mouth2_base64,
                    face_contoured1, face_contoured2, img1_embeddings, img2_embeddings):
    with open('report_templates/standard.html', 'r') as file:
        report_standard_cache = file.read()
        file.close()

    with open('face_comparison_report.html', 'w+') as file:
        img1_base64 = str(img1_base64).rstrip("'")
        img2_base64 = str(img2_base64).rstrip("'")
        report_standard_cache = report_standard_cache.replace("##base64_img1##", img1_base64.replace("b'", ""))
        report_standard_cache = report_standard_cache.replace("##base64_img2##", img2_base64.replace("b'", ""))
        report_standard_cache = report_standard_cache.replace("##facenet_score##", str(round(facenet_score, 2)))
        report_standard_cache = report_standard_cache.replace("##sface_score##", str(round(sface_score, 2)))
        if facenet_verif == True:
            report_standard_cache = report_standard_cache.replace("##color_facenet##", "green")
            report_standard_cache = report_standard_cache.replace("##facenet_note##", "The AI sees these two faces as the same person based on the Facenet model.")
        else:
            report_standard_cache = report_standard_cache.replace("##color_facenet##", "red")
            report_standard_cache = report_standard_cache.replace("##facenet_note##", "The AI sees these two faces as a different person based on the Facenet model.")
        if sface_verif == True:
            report_standard_cache = report_standard_cache.replace("##color_sface##", "green")
            report_standard_cache = report_standard_cache.replace("##sface_note##", "The AI sees these two faces as the same person based on the SFace model.")
        else:
            report_standard_cache = report_standard_cache.replace("##color_sface##", "red")
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

        file.write(report_standard_cache)
        file.close()
    