import render.ImageGenerator
import sys
from PIL import Image
import flask
import os

app=flask.Flask(__name__)
mappings = {90: Image.ROTATE_90, 190: Image.ROTATE_180, 270: Image.ROTATE_270}

#http://localhost:5000/Jules+Verne+-+Reise+um+die+Erde+in+80+Tagen.epub/600/800/10/14/90/39.pbm
@app.route('/<file>/<int:panel_width>/<int:panel_height>/<int:border>/<int:fontSizeInPx>/<int:amount>/<int:page>.<type>')
def epubOnDemandRender(file, panel_width, panel_height, border, fontSizeInPx, amount,type,page):
    print(file)
    print(panel_width)
    print(panel_height)
    print(border)
    print(fontSizeInPx)
    print(amount)
    print(os.path.dirname(os.path.realpath('.')))
    imageGenerator = render.ImageGenerator.ImageGenerator()
    transpose=Image.ROTATE_90
    transpose=mappings.get(amount,Image.ROTATE_90)
    tmpPath='tmp/'+file+'/'+str(panel_width)+'/'+str(panel_height)+'/'+str(border)+'/'+str(fontSizeInPx)+'/'+str(amount)
    imageGenerator.preRenderBook(
        'books/'+file, panel_width,panel_height,
        (border,border,border,border+10), fontSizeInPx,transpose,tmpPath,'.'+type,page)
    smallImgName = tmpPath + '/' + (str(page)) + '.'+type
    print(smallImgName)
    return flask.send_file(smallImgName, mimetype='image/'+type)

def main():

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

