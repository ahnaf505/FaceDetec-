

report_standard_cache = ""

def generate_report(img1_base64, img2_base64, img1_name, img2_name):
    with open('report_templates/standard.html', 'r') as file:
        report_standard_cache = file.read()
        file.close()

    with open('face_comparison_report.html', 'w+') as file:
        img1_base64 = str(img1_base64).rstrip("'")
        img2_base64 = str(img2_base64).rstrip("'")
        report_standard_cache = report_standard_cache.replace("##base64_img1##", img1_base64.replace("b'", ""))
        report_standard_cache = report_standard_cache.replace("##base64_img2##", img2_base64.replace("b'", ""))
        report_standard_cache = report_standard_cache.replace("##img1_name##", str(img1_name))
        report_standard_cache = report_standard_cache.replace("##img2_name##", str(img2_name))
        report_standard_cache = report_standard_cache.replace("##facenet_score##, str(img2_name))
        file.write(report_standard_cache)
        file.close()
    