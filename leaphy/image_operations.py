from picamera2 import Picamera2
import numpy as np
import tensorflow as tf

def setup_camera():
    camera = Picamera2()
    cam_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (64, 64)})
    camera.configure(cam_config)
    camera.start_preview()
    camera.start()
    return camera

def picture():
    #take picture and save
    camera.capture_file("input_image.jpg")

def load_image():
    #load picture into memory and format
    img = tf.io.read_file("input_image.jpg")
    img = tf.image.decode_jpeg(img)
    img = np.array(img)
    return img

def line_image(img, parts):
    #crop image for line searching
    height, width = img.shape[0], img.shape[1]
    while True:
        if (width/2/parts).is_integer():
            width_size = width/2
            break
        else:
            width_size = int(int(width/2/parts)*parts/2)

    img = img.copy()[(int(height*0.9)):height, (int((width/2)-width_size)):(int((width/2)+width_size))]
    img = tf.image.rgb_to_grayscale(img)
    img = np.array(img)
    return img

def model_image(img, compression):
    #crop and resize image for model execution
    height, width = img.shape[0], img.shape[1]
    width /= compression
    height /= compression
    img = img.copy()
    img = img.reshape(width/2, height, 3)
    img = np.array(img)[np.newaxis,...]
    return img

def shutdown():
    camera.stop_preview()

#setup the camera
camera = setup_camera()