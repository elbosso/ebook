import imgkit
import os
import ebooklib
import zipfile
from PIL import Image, ImageDraw, ImageFont
from ebooklib import epub
from ebooklib.utils import debug


class ImageGenerator:
    """First test at packaging"""

    imgCounter=0
    cssFileName = "/tmp/ebook.css"

    def preRenderBook(self, fileWithPath, panel_width, panel_height, border, fontSizeInPx,transpose):
        imgCounter=0

        css=open(self.cssFileName, "w")
        css.write('html {font-size: '+str(fontSizeInPx)+'px;}')
        css.close()

        zip_ref = zipfile.ZipFile(fileWithPath, 'r')
        zip_ref.extractall('/tmp/book')
        zip_ref.close()
        book = epub.read_epub(fileWithPath)

        debug(book.metadata)
        debug(book.spine)
        debug(book.toc)

        debug('================================')
        debug('DOCUMENTS')

        for x in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            if x.is_chapter():
                self.preRenderChapter('/tmp/book/' + 'OPS/' + x.get_name(), panel_width, panel_height, border,transpose)
        debug('================================')
        os.remove(self.cssFileName)


    def preRenderChapter(self, fileWithName, panel_width, panel_height, border,transpose):
        bl,br,bt,bb=border
        height=panel_height-bt-bb
        width=panel_width-bl-br
        options = {
            'format': 'png',
            'width': str(panel_width),
            'user-style-sheet': self.cssFileName
        }
        chapter_image='/tmp/out.png'
        imgkit.from_url(fileWithName, chapter_image,options=options)
        im = Image.open('/tmp/out.png')
        iwidth, iheight = im.size
        off=0
        while(off<iheight):
            options = {
                'format': 'png',
                'crop-h': str(height),
                'crop-y': str(off),
                'width':str(width),
                'user-style-sheet': self.cssFileName
            }
            smallImgName='/tmp/'+(str(self.imgCounter))+'.pbm'
            imgkit.from_url(fileWithName, smallImgName,options=options)
            off=off+height
            im = Image.open(smallImgName)
            im = im.convert('L')

            pixels = list(im.getdata())
            pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

            black_lines = 0
            for line in reversed(pixels):
                black_count = len([x for x in line if x <= 1])
                if (black_count ) > 0:
                    black_lines += 1
                else:
                    break
            if(black_lines>0):
                off=off-black_lines-2

            newImage = Image.new('L', (panel_width,panel_height), 255)
            newImage.paste(im.crop((0,0,width,height-black_lines)), (bl, bt))
            button_draw = ImageDraw.Draw(newImage)
            owidth, oheight = im.size
            if(oheight<height):
                xy=[bl,bt+oheight,bl+width,bt+height]
                button_draw.rectangle(xy,fill=(255))
            button_draw.text((width/2, height+bt+1), str(self.imgCounter), font=ImageFont.truetype("DejaVuSans",bb-2), fill=(1))
            del button_draw

            if(transpose is not None):
                newImage=newImage.transpose(transpose)
            newImage=newImage.convert('1')
            newImage.save(smallImgName)
            self.imgCounter = self.imgCounter + 1
            print(smallImgName);
        os.remove(chapter_image)
