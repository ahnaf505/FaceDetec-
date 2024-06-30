from colorama import *
import colorama
from compare import *

colorama.init(autoreset=True)
just_fix_windows_console()
print(colorama.ansi.clear_screen())
print(Back.BLACK + Fore.BLUE + "FaceDetec' | CLI Interface")
print(Back.WHITE + "Press enter to start making a face comparison report...")
input()

img1_pth = input("Please input path for the first face image: ")
img2_pth = input("Please input path for the second face image: ")

