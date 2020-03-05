import time, os
import cv2
from flask import Flask, flash, request, redirect, url_for, render_template, Response, jsonify
from werkzeug.utils import secure_filename
import re, time, base64
import numpy as np
from face_modules.single_face_detection import compare_two_img
# import base64

app = Flask(__name__, static_url_path='/static')


def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def base64_to_image(base64_image, img_path_one):
    try:
        encoded_data = base64_image.split(',')[1]
        imgdata = base64.b64decode(encoded_data)
        # print('imgdata', imgdata)
        with open(img_path_one, 'wb') as f:
            f.write(imgdata)
        f.close()
        return True
    except Exception as error:
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

            img_path_one = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_one.jpg"
            img_path_two = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_two.jpg"

            
            image_one = base64_to_image(base64_image_one, img_path_one)
            image_two = base64_to_image(base64_image_two, img_path_two)

            # cv2.imwrite(img_path_one, image_one)
            # cv2.imwrite(img_path_two, image_two)

            distance = compare_two_img(img_path_one, img_path_two)

            return jsonify({"is_success": True, "distance": distance})
        except Exception as error:
            return jsonify({"is_success": False, "message": "Please provide a valid single face image"})


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)