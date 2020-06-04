import pydicom
from PIL import Image
import numpy as np
import cv2
import os
import tensorflow as tf

def read_dicom(file):
    data = pydicom.dcmread(file)
    pixels = data.pixel_array
    return (pixels//16).astype('uint8')


def dicom2png(path, save_path):
    for file in os.listdir(path):
        name = os.path.splitext(file)[0]
        img = read_dicom(os.path.join(path, file))
        Image.fromarray(img).save(os.path.join(save_path, f"{name}.png"))

def decode_img(img):
    img = tf.image.decode_png(img, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    return tf.image.resize(img, [IMG_SIZE, IMG_SIZE])