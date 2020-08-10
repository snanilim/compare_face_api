import time, os
import cv2
from flask import Flask, flash, request, redirect, url_for, render_template, Response, jsonify, Blueprint
from werkzeug.utils import secure_filename
import re, time, base64
import numpy as np
from two_face_compare_api.face_modules.single_face_detection import compare_two_img
import PIL
from PIL import Image, ExifTags, ImageOps
from io import BytesIO
from two_face_compare_api.utils.helper import data_uri_to_cv2_img, get_ext, rotate_image, resize_image, base64_to_image, delete_files
from two_face_compare_api.utils import face_logger
import uuid
import time
from datetime import datetime
from flask import g
# import base64

app = Blueprint('app', __name__)
logger = face_logger.log_fun()

@app.route('/')
def index():
    return {"message": "Two Face Comare Api"}

@app.route('/compare_two_pic', methods=['GET', 'POST'])
def compare_two_pic_api():
    if request.method == 'GET':
        return jsonify({"message": "This is a post request pleasy try with a post request"})
    if request.method == 'POST':
        try:
            unq_id = uuid.uuid4()
            start_time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            g.start = time.time()
            logger.info({"process":"start", "message": "Start Face Match processing", "uuid": unq_id, "start_time": start_time})



            UPLOAD_FOLDER_TWO_IMG = '/var/www/ekyc_two_face_compare/two_face_compare_api/static/compare_two_img'

            data = request.get_json()
            base64_image_one = request.get_json()['img_one']

            img_name = 'img_two'
            if 'img_nid' in data.keys():
                img_name = 'img_nid'
                base64_image_two = request.get_json()['img_nid']
            else:
                base64_image_two = request.get_json()['img_two']


            img_path_one = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_one.jpg"
            img_path_two = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_two.jpg"

            delete_files()
            
            image_one = base64_to_image(base64_image_one, img_path_one, 'img_one')
            image_two = base64_to_image(base64_image_two, img_path_two, img_name)


            distance = compare_two_img(img_path_one, img_path_two)
            print('distance', distance)

            end_time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            logger.info({"process":"end", "message": "End Face Match processing with Success", "uuid": unq_id, "end_time": end_time, "total_time": time.time() - g.start})

            delete_files()
            return jsonify({"is_success": True, "distance": distance})


        except ValueError as error:
            print('compare ValueError', error)
            end_time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            logger.error({"process":"end", "message": error, "uuid": unq_id, "end_time": end_time, "total_time": time.time() - g.start})
            return jsonify({"is_success": False, "message": str(error)})


        except Exception as error:
            print('else imgToOcr', error)
            end_time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            logger.error({"process":"end", "message": error, "uuid": unq_id, "end_time": end_time, "total_time": time.time() - g.start})
            return jsonify({"is_success": False, "message": "Failed to compare two face. please try again"})


@app.route('/test_compare_two_pic', methods=['GET', 'POST'])
def test_compare_two_pic_api():
    if request.method == 'GET':
        UPLOAD_FOLDER_TWO_IMG = '/var/www/ekyc_two_face_compare/two_face_compare_api/static/test_compare_two_img'

        img_path_one = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_one.jpg"
        img_path_two = f"{UPLOAD_FOLDER_TWO_IMG}/compare_img_two.jpg"
        distance = compare_two_img(img_path_one, img_path_two)
        return jsonify({"is_success": True, "distance": distance})

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)