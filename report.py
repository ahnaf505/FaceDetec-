

report_standard_cache = ""

def generate_report(img1_base64, img2_base64, facenet_score, facenet_verif, 
                    leye1_base64, reye1_base64, nose1_base64, mouth1_base64):
    with open('report_templates/standard.html', 'r') as file:
        report_standard_cache = file.read()
        file.close()

    with open('face_comparison_report.html', 'w+') as file:
        img1_base64 = str(img1_base64).rstrip("'")
        img2_base64 = str(img2_base64).rstrip("'")
        report_standard_cache = report_standard_cache.replace("##base64_img1##", img1_base64.replace("b'", ""))
        report_standard_cache = report_standard_cache.replace("##base64_img2##", img2_base64.replace("b'", ""))
        report_standard_cache = report_standard_cache.replace("##facenet_score##", str(round(facenet_score, 2)))
        if facenet_verif == True:
            report_standard_cache = report_standard_cache.replace("##color_facenet##", "green")
            report_standard_cache = report_standard_cache.replace("##facenet_note##", "The AI sees these two faces as the same person based on the Facenet model.")
        else:
            report_standard_cache = report_standard_cache.replace("##color_facenet##", "red")
            report_standard_cache = report_standard_cache.replace("##facenet_note##", "The AI sees these two faces as a different person based on the Facenet model.")
        report_standard_cache = report_standard_cache.replace("##base64_img1_leye##", leye1_base64)
        report_standard_cache = report_standard_cache.replace("##base64_img1_reye##", reye1_base64)
        report_standard_cache = report_standard_cache.replace("##base64_img1_nose##", nose1_base64)
        report_standard_cache = report_standard_cache.replace("##base64_img1_mouth##", mouth1_base64)
        
        file.write(report_standard_cache)
        file.close()
    