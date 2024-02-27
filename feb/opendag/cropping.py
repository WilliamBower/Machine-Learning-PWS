import tensorflow as tf
import numpy as np

trigger_range_x = 0
trigger_range_y = 500
trigger_range_height = 540
trigger_range_width = 1920

img = tf.io.read_file("C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/feb/opendag/input_image.jpg")
img = tf.image.decode_jpeg(img)
img = tf.image.rot90(img, k=2)
img = np.array(img)
img = img[:, :, :3]
img = img[trigger_range_y:(trigger_range_y+trigger_range_height), trigger_range_x:(trigger_range_x+trigger_range_width)]
print(img.shape)
tf.keras.utils.save_img("input_image2.jpg", img)