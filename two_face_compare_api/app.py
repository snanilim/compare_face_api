import time, os
import cv2
from flask import Flask, flash, request, redirect, url_for, render_template, Response, jsonify
from werkzeug.utils import secure_filename
import re, time, base64
import numpy as np
from face_modules.single_face_detection import compare_two_img
import PIL
from PIL import Image, ExifTags, ImageOps
from io import BytesIO
from helper import data_uri_to_cv2_img, get_ext, rotate_image, resize_image, base64_to_image
# import base64

app = Flask(__name__, static_url_path='/static')

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

            data = request.get_json()
            base64_image_one = request.get_json()['img_one']

            print('img_nid', 'img_nid' in request.args)
            print('request.args', data.keys())
            print('request.args', 'img_nid' in data.keys())

            img_name = 'img_two'
            if 'img_nid' in data.keys():
                img_name = 'img_nid'
                base64_image_two = request.get_json()['img_nid']
            else:
                base64_image_two = request.get_json()['img_two']

            
            # print('img_two', request.get_json()['img_two'])

            # ext_one = get_ext(base64_image_one)
            # ext_two = get_ext(base64_image_two)

            img_path_one = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_one.jpg"
            img_path_two = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_two.jpg"

            
            image_one = base64_to_image(base64_image_one, img_path_one, 'img_one')
            image_two = base64_to_image(base64_image_two, img_path_two, img_name)

            # cv2.imwrite(img_path_one, image_one)
            # cv2.imwrite(img_path_two, image_two)

            distance = compare_two_img(img_path_one, img_path_two)
            print('distance', distance)
            return jsonify({"is_success": True, "distance": distance})
        except Exception as error:
            print('compare_two_pic_api', error)
            return jsonify({"is_success": False, "message": "Please provide a valid single face image"})


@app.route('/test_compare_two_pic', methods=['GET', 'POST'])
def test_compare_two_pic_api():
    if request.method == 'GET':
        UPLOAD_FOLDER_TWO_IMG = 'static/test_compare_two_img'

        img_path_one = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_one.jpg"
        img_path_two = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_two.jpg"
        distance = compare_two_img(img_path_one, img_path_two)
        return jsonify({"is_success": True, "distance": distance})

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)