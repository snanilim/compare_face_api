import time, os
import cv2
from flask import Flask, flash, request, redirect, url_for, render_template, Response, jsonify
from werkzeug.utils import secure_filename
import re, time, base64
import numpy as np
from face_modules.single_face_detection import compare_two_img
from PIL import Image, ExifTags, ImageOps
from io import BytesIO
# import base64

app = Flask(__name__, static_url_path='/static')


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
            image.convert('RGB').save(img_path)
        else:
            im.convert('RGB').save(img_path)
        return True
    except Exception as error:
        print('base64_to_image', error)
        return error

@app.route('/')
def index():
    return {"message": "Two Face Comare Api"}

@app.route('/compare_two_pic', methods=['GET', 'POST'])
def compare_two_pic_api():
    if request.method == 'GET':
        return jsonify({"message": "This is a post request pleasy try with a post request"})
    if request.method == 'POST':
        try:
            UPLOAD_FOLDER_TWO_IMG = 'static/compare_two_img'

            base64_image_one = request.get_json()['img_one']
            base64_image_two = request.get_json()['img_two']

            ext_one = get_ext(base64_image_one)
            ext_two = get_ext(base64_image_two)

            print('ext_one', ext_one)

            img_path_one = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_one.jpg"
            img_path_two = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_two.jpg"

            
            image_one = base64_to_image(base64_image_one, img_path_one)
            image_two = base64_to_image(base64_image_two, img_path_two)

            # cv2.imwrite(img_path_one, image_one)
            # cv2.imwrite(img_path_two, image_two)

            distance = compare_two_img(img_path_one, img_path_two)
            print('distance', distance)
            return jsonify({"is_success": True, "distance": distance})
        except Exception as error:
            return jsonify({"is_success": False, "message": "Please provide a valid single face image"})


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)