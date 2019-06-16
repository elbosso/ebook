import render.ImageGenerator
import sys
from PIL import Image

def main():
    mappings = {90: Image.ROTATE_90,190: Image.ROTATE_180,270: Image.ROTATE_270}

    imageGenerator = render.ImageGenerator.ImageGenerator()
    transpose=Image.ROTATE_90
    if (len(sys.argv) >9):
        amount=int(sys.argv[9])
        transpose=mappings.get(amount,Image.ROTATE_90)
    imageGenerator.preRenderBook(
        sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
        (int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])), int(sys.argv[8]),transpose)

def help():
    print("call the script with the following parameters please:")
    print("epub (file name including path)")
    print("horizontal resolution of display in pixels (int)")
    print("vertical  resolution of display in pixels (int)")
    print("left margin in pixels (int)")
    print("right margin in pixels  (int)")
    print("top margin in pixels  (int)")
    print("bottom margin in pixels  (int)")
    print("Font size for text (int)")
    print("[Rotation for final image (counterclockwise, int - allowed values are 0,90,180,270, default is 90)]")
if __name__ == "__main__":
    if(len(sys.argv)<9):
        help()
    else:
        main()

