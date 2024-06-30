

report_standard_cache = ""

def generate_report(img1_base64, img2_base64, img1_name, img2_name):
    with open('/report_templates/standard.html', 'r') as file:
        report_standard_cache = file.read()
        file.close()

    with open('face_comparison_report.html', 'w+') as file:
        report_standard_cache = report_standard_cache.replace("##base64_img1##", img1_base64)
        report_standard_cache = report_standard_cache.replace("##base64_img2##", img2_base64)
        report_standard_cache = report_standard_cache.replace("##img1_name##", img1_name)
        report_standard_cache = report_standard_cache.replace("##img2_name##", img2_name)
        file.write(report_standard_cache)
        file.close()
    