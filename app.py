import colorama
from colorama import *
from report import *
from processing import *
from validator import *
import sys
import time

colorama.init(autoreset=True)

just_fix_windows_console()

time.sleep(2)

print(colorama.ansi.clear_screen())
print(Back.BLACK + Fore.BLUE + "FaceDetec' | CLI Interface")

print(Back.WHITE + "Press enter to start making a face comparison report...")
input('\n')

img1_pth = input("Please input path for the first face image: ")
img2_pth = input("Please input path for the second face image: ")

if is_file_exists(img1_pth) != True:
    print("Image 1 did not exist or is not an image...")
    sys.exit()

elif is_file_exists(img2_pth) != True:
    print("Image 2 did not exist or is not an image...")
    sys.exit()
else:
    print("Image files successfully verified...\n")

print("Running face comparison processing...")
compare_output = run_compare(img1_pth, img2_pth)

if compare_output == "err1":
    print("No face detected even after 50 times retry")
    sys.exit()

print("Processing face features on Image 1...")
face_cutted1 = cutout_face_features(img1_pth)
print("Successfully processed face features on Image 1...")

print("Processing face features on Image 2...")
face_cutted2 = cutout_face_features(img2_pth)
print("Successfully processed face features on Image 2...\n")

print("Detecting and cropping face on Image 1...")
img1_base64 = detect_and_crop_face(img1_pth)
print("Successfully detected and cropped face on Image 1...")

print("Detecting and cropping face on Image 2...")
img2_base64 = detect_and_crop_face(img2_pth)
print("Successfully detected and cropped face on Image 2...\n")

print("Calculating face embeddings on Image 1...")
img1_embeddings = face_embeddings_extract(img1_pth)
print("Successfully calculated face embeddings on Image 1...")

print("Calculating face embeddings on Image 2...")
img2_embeddings = face_embeddings_extract(img2_pth)
print("Successfully calculated face embeddings on Image 2...\n")

print("Detecting face contour on Image 1...")
face_contoured1 = draw_skin_contour(img1_base64)
print("Successfully detected face contour on Image 1...")

print("Detecting face contour on Image 2...")
face_contoured2 = draw_skin_contour(img2_base64)
print("Successfully detected face contour on Image 2...\n")

print("Generating report...")
reportid = generate_report(img1_base64, img2_base64, compare_output[1], compare_output[0],
                           compare_output[2], compare_output[3],
                           face_cutted1[0], face_cutted1[1], face_cutted1[2], face_cutted1[3],
                           face_cutted2[0], face_cutted2[1], face_cutted2[2], face_cutted2[3],
                           face_contoured1, face_contoured2, img1_embeddings, img2_embeddings)

print(f"Successfully generated face comparison report [face_comparison_report - {reportid}.html]")
