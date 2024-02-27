from picamera2 import Picamera2
import numpy as np
import math
import tensorflow as tf

def setup_camera():
	print("Cam setup start")
	camera = Picamera2()
	cam_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (64, 64)})
	camera.configure(cam_config)
	camera.start_preview()
	camera.start()
	print("Cam setup complete")
	return camera

def picture(image_path = "input_image.jpg"):
	camera.capture_file(image_path)

def load_image(image_path = "input_image.jpg"):
	img = tf.io.read_file(image_path)
	img = tf.image.decode_jpeg(img)
	img = tf.image.rot90(img, k=2)
	img = np.array(img)
	return img

def line_image(img, parts):
	height, width = img.shape[0], img.shape[1]
#	print(4)
	width_size = width/2
	width_size = int(math.floor(width_size/parts)*parts)
#	print(5)
	img = img.copy()[(int(height*0.9)):height, (int((width/2)-width_size)):(int((width/2)+width_size))]
	img = tf.image.rgb_to_grayscale(img)
	img = np.array(img)
	return img

def shutdown():
	camera.stop_preview()

camera = setup_camera()
