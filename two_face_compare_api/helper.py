import time, os
import cv2
from werkzeug.utils import secure_filename
import re, time, base64
import numpy as np
from face_modules.single_face_detection import compare_two_img
import PIL
from PIL import Image, ExifTags, ImageOps
from io import BytesIO

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_ext(uri):
    ext = uri.split(',')[0].split('/')[1].split(';')[0]
    print('firstData', ext)
    return ext

def rotate_image(im):
    try:
        image = ImageOps.exif_transpose(im)
        # print('image', image)
        # for orientation in ExifTags.TAGS.keys():
        #     if ExifTags.TAGS[orientation]=='Orientation':
        #         break
        # exif=dict(im._getexif().items())
        # print('exif[orientation]', exif[orientation])
        # if exif[orientation] == 3:
        #     im=im.rotate(180, expand=True)
        # elif exif[orientation] == 6:
        #     im=im.rotate(270, expand=True)
        # elif exif[orientation] == 8:
        #     im=im.rotate(90, expand=True)

        return image
    except Exception as error:
        print('error_rotate_image', error)
        return False

def resize_image(image):
    try:
        basewidth = 300
        if float(image.size[0]) > basewidth:
            wpercent = (basewidth / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(wpercent)))
            image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
            return image
        else:
            return image
    except Exception as error:
        print('resize_image', error)
        return False


def base64_to_image(base64_image, img_path):
    try:
        # print('base64_image', base64_image)
        encoded_data = base64_image.split(',')[1]
        # imgdata = base64.b64decode(encoded_data)
        # # print('imgdata', imgdata)
        # with open(img_path, 'wb') as f:
        #     f.write(imgdata)
        # f.close()
        ext = get_ext(base64_image)
        im = Image.open(BytesIO(base64.b64decode(encoded_data)))
        image = rotate_image(im)

        if image:
            reImg = resize_image(image)
        else:
            reImg = resize_image(im)
        reImg.convert('RGB').save(img_path)
        return True
    except Exception as error:
        print('base64_to_image', error)
        return error