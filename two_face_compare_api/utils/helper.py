import time, os
import cv2
from werkzeug.utils import secure_filename
import re, time, base64
import numpy as np
# from face_modules.single_face_detection import compare_two_img, save_image_for_nid
import PIL
from PIL import Image, ExifTags, ImageOps
from io import BytesIO


def delete_files():
    try:
        print('Deleted All files')
        # delete all files from a folder
        delDir = '/var/www/ekyc_two_face_compare/two_face_compare_api/static/compare_two_img'
        filelist = [ f for f in os.listdir(delDir) if f.endswith(".jpg") ]
        for f in filelist:
            os.remove(os.path.join(delDir, f))
    except Exception as error:
        print('delete_files', error)
        return error

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_ext(uri):
    ext = uri.split(',')[0].split('/')[1].split(';')[0]
    print('firstData', ext)
    return ext

def rotate_image(im, img_name):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(im._getexif().items())
        print('exif[orientation]', exif[orientation])
        if exif[orientation] == 3:
            im=im.rotate(180, expand=True)
        elif exif[orientation] == 6:
            im=im.rotate(270, expand=True)
        elif exif[orientation] == 8:
            im=im.rotate(90, expand=True)

        return im
    except Exception as error:
        print('error_rotate_image', error)
        return False

def resize_image(image, img_name):
    try:
        if img_name == 'img_nid':
            basewidth = 650
        else:
            basewidth = 300

        if float(image.size[0]) > basewidth:
            print(image.size[0])
            wpercent = (basewidth / float(image.size[0]))
            print(wpercent)
            hsize = int((float(image.size[1]) * float(wpercent)))
            print(hsize)
            image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
            return image
        else:
            return image
    except Exception as error:
        print('resize_image', error)
        return False

# def nid_resize():
    # if img_name == 'img_nid':
    #     image = save_image_for_nid(img_path)
    #     height, width, channels = image.shape
        
    #     basewidth = 110
    #     if width > basewidth:
    #         print(width)
    #         wpercent = ((basewidth * 100) / width)
    #         print(wpercent)
    #         hsize = int((height * wpercent) / 100)
    #         print(hsize)
    #         image = cv2.resize(image, (basewidth, hsize)) 

    #     cv2.imwrite(img_path, image)
        # image = cv2.imread(img_path)


def base64_to_image(base64_image, img_path, img_name):
    try:
        # print('base64_image', base64_image)
        encoded_data = base64_image.split(',')[1]
        ext = get_ext(base64_image)
        im = Image.open(BytesIO(base64.b64decode(encoded_data)))
        image = rotate_image(im, img_name)
        if image:
            reImg = resize_image(image, img_name)
        else:
            reImg = resize_image(im, img_name)
        reImg.convert('RGB').save(img_path)

        return True
    except Exception as error:
        print('base64_to_image', error)
        raise ValueError(str(error) + ". " + "Failed to convert base64 to image. Please provide a valid base64 image")