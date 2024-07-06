# Import necessary modules
import colorama
from colorama import *
from report import *
from processing import *
from validator import *
import sys
import time

# Initialize colorama for colored output in terminals
colorama.init(autoreset=True)

# Adjust console for Windows compatibility
just_fix_windows_console()

# Pause for 2 seconds for visibility
time.sleep(2)

# Clear the console screen
print(colorama.ansi.clear_screen())

# Print header for the CLI interface
print(Back.BLACK + Fore.BLUE + "FaceDetec' | CLI Interface")

# Prompt user to start face comparison report generation
print(Back.WHITE + "Press enter to start making a face comparison report...")
input('\n')

# Prompt user for paths to two face images
img1_pth = input("Please input path for the first face image: ")
img2_pth = input("Please input path for the second face image: ")

# Check if the first image exists and is an image file
if is_file_exists(img1_pth) != True:
    print("Image 1 did not exist or is not an image...")
    sys.exit()
# Check if the second image exists and is an image file
elif is_file_exists(img2_pth) != True:
    print("Image 2 did not exist or is not an image...")
    sys.exit()
else:
    print("Image files successfully verified...")

# Start face comparison processing
print("Running face comparison processing...")
compare_output = run_compare(img1_pth, img2_pth)

# Handle case where no face is detected in either image
if compare_output == "err1":
    print("No face detected even after 50 times retry")
    sys.exit()

# Process face features for Image 1
print("Processing face features on Image 1...")
face_cutted1 = cutout_face_features(img1_pth)
print("Successfully processed face features on Image 1...")

# Process face features for Image 2
print("Processing face features on Image 2...")
face_cutted2 = cutout_face_features(img2_pth)
print("Successfully processed face features on Image 2...\n")

# Detect and crop face from Image 1
print("Detecting and cropping face on Image 1...")
img1_base64 = detect_and_crop_face(img1_pth)
print("Successfully detected and cropped face on Image 1...")

# Detect and crop face from Image 2
print("Detecting and cropping face on Image 2...")
img2_base64 = detect_and_crop_face(img2_pth)
print("Successfully detected and cropped face on Image 2...\n")

# Calculate face embeddings for Image 1
print("Calculating face embeddings on Image 1...")
img1_embeddings = face_embeddings_extract(img1_pth)
print("Successfully calculated face embeddings on Image 1...")

# Calculate face embeddings for Image 2
print("Calculating face embeddings on Image 2...")
img2_embeddings = face_embeddings_extract(img2_pth)
print("Successfully calculated face embeddings on Image 2...\n")

# Detect face contours for Image 1
print("Detecting face contour on Image 1...")
face_contoured1 = draw_skin_contour(img1_base64)
print("Successfully detected face contour on Image 1...")

# Detect face contours for Image 2
print("Detecting face contour on Image 2...")
face_contoured2 = draw_skin_contour(img2_base64)
print("Successfully detected face contour on Image 2...\n")

# Generate face comparison report
print("Generating report...")
reportid = generate_report(img1_base64, img2_base64, compare_output[1], compare_output[0],
                           compare_output[2], compare_output[3],
                           face_cutted1[0], face_cutted1[1], face_cutted1[2], face_cutted1[3],
                           face_cutted2[0], face_cutted2[1], face_cutted2[2], face_cutted2[3],
                           face_contoured1, face_contoured2, img1_embeddings, img2_embeddings)

# Print success message with generated report ID
print(f"Successfully generated face comparison report [face_comparison_report - {reportid}.html]")
