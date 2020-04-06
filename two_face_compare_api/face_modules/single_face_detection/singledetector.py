from . import DetectionToolKit as dtk
from . import FaceToolKit as ftk
import time
import tensorflow as tf
import numpy as np
import cv2
from .detection.mtcnn import detect_face
import matplotlib.pyplot as plt
from scipy import misc
import os, pickle


with tf.Graph().as_default():
    sess = tf.Session()
    pnet, rnet, onet = detect_face.create_mtcnn(sess, None)

default_color = (0, 255, 0)  # BGR
default_thickness = 2

minsize = 20  # minimum size of face
threshold = [0.6, 0.7, 0.7]  # three steps's threshold
factor = 0.709  # scale factor


# verify image
# import face_modules.single_face_detection.FaceToolKit as ftk

verification_threshhold = 0.9
image_size = 160
v = ftk.Verification()
# Pre-load model for Verification
v.load_model("static/models/0180204-160909/")
v.initial_input_output_tensors()


d = dtk.Detection()

def img_to_encoding_db(img):
    try:
        image = plt.imread(img)
        print('img')
        aligned = d.align(image, False)[0]
        # print('aligned', aligned)
        # cv2.imwrite("./aligned_n.jpg", aligned)
        return v.img_to_encoding(aligned, image_size)
    except Exception as error:
        print('img_to_encoding_db', error)
        return error

def save_image_for_nid(img):
    try:
        img = plt.imread(img)
        aligned = d.nid_align(img, False)
        return aligned
    except Exception as error:
        print('save_image_for_nid', error)
        return error


def distance(emb1, emb2):
    try:
        diff = np.subtract(emb1, emb2)
        return np.sum(np.square(diff))
    except Exception as error:
        return error



def compare_two_img(image_one, image_two):
    try:
        print('call')
        enc_one = img_to_encoding_db(image_one)
        enc_two = img_to_encoding_db(image_two)

        dist = distance(enc_one, enc_two)

        return dist
    except Exception as error:
        return error

