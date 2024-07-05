import colorama
import base64
from PIL import Image
from colorama import *
from report import *
from processing import *
import sys
import time

colorama.init(autoreset=True)

just_fix_windows_console()
time.sleep(2)
print(colorama.ansi.clear_screen())
print(Back.BLACK + Fore.BLUE + "FaceDetec' | CLI Interface")
print(Back.WHITE + "Press enter to start making a face comparison report...")
input('\n')

print('NOTE: THIS APP ONLY SUPPORTS JPG FORMAT')
img1_pth = input("Please input path for the first face image: ")
img2_pth = input("Please input path for the second face image: ")

compare_output = run_compare(img1_pth, img2_pth)

if compare_output == "err1":
    print("No face detected or other error has occoured")
    sys.exit()
else:
    pass

face_cutted1 = cutout_face_features(img1_pth)
face_cutted2 = cutout_face_features(img2_pth)
img1_base64 = detect_and_crop_face(img1_pth)
img2_base64 = detect_and_crop_face(img2_pth)

img1_embeddings = face_embeddings_extract(img1_pth)

face_contoured1 = draw_skin_contour(img1_base64)
face_contoured2 = draw_skin_contour(img2_base64)
generate_report(img1_base64, img2_base64, compare_output[1], compare_output[0],
                compare_output[2], compare_output[3] ,
                face_cutted1[0], face_cutted1[1], face_cutted1[2], face_cutted1[3],
                face_cutted2[0], face_cutted2[1], face_cutted2[2], face_cutted2[3],
                face_contoured1, face_contoured2, img1_embeddings)
