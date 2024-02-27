import numpy as np
import tensorflow as tf
from PIL import Image

trigger_range_x = 0
trigger_range_y = 0
trigger_range_height = 100
trigger_range_width = 100
green_threshold = 50

def load_image():
    #load picture into memory and format
    img = tf.io.read_file("input_image.jpg")
    img = tf.image.decode_jpeg(img)
    img = img.rotate(180)
    img = np.array(img)
    return img

def trigger_image(img):
    img = img[trigger_range_y:(trigger_range_y+trigger_range_height), trigger_range_x:(trigger_range_x+trigger_range_width)]
    red, green, blue = img.split()
    del red, blue
    img2 = Image.merge("RGB", (0, green, 0))
    green_pixels = np.sum(img2 <= green_threshold)
    return green_pixels, img2