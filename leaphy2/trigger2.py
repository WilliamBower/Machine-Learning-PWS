import numpy as np
import tensorflow as tf
from PIL import Image

trigger_range_x = 0
trigger_range_y = 0
trigger_range_height = 540
trigger_range_width = 1920
lower_green = np.array([225, 9, 21])
higher_green = np.array([227, 11, 23])
min_green_count = 50
compression = 10

def load_image():
    #load picture into memory and format
    #img = Image.open("C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/test/image0.jpeg")
    img = tf.io.read_file("C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/20_small.png")
    img = tf.image.decode_jpeg(img)
    #img = tf.image.rot90(img, k=2)
    img = np.array(img)
    img = img[:, :, :3]
    print(img.shape)
    return img

def trigger_image(img):
    print("Creating Mask")
    img = img[trigger_range_y:(trigger_range_y+trigger_range_height), trigger_range_x:(trigger_range_x+trigger_range_width)]
    img2 = np.all((img >= lower_green) & (img <= higher_green), axis=-1)
    result = np.zeros_like(img)
    result[img2] = img[img2]
    print("Mask created")
    return result, img

def locate_green(mask, img):
    print("Locating")
    height, width = mask.shape[0], mask.shape[1]
    bottom_y = 0
    top_y = 0
    left_x = 0
    right_x = 0
    print(mask.max())
    if mask.max() == 0:
        print("No Green found")
        return None

    for i in range(height):
        a = mask.copy()[(height-i-1):(height-i), 0:width]
        if a.max() > 0:
            bottom_y = height - i
            break
    print("Bottom Y found")
    #img = img[0:bottom_y, 0:width]
    mask = mask[0:bottom_y, 0:width]
    height, width = mask.shape[0], mask.shape[1]
    for i in range(width):
        a = mask.copy()[0:height, i:(i+1)]
        if a.max() > 0:
            left_x = i
            break
    print("Left X found")
    for i in range(width):
        a = mask.copy()[0:height, (width-i-1):(width-i)]
        if a.max() > 0:
            right_x = width - i
            break
    print("Right X found")
    green_width = right_x - left_x
    #img = img[0:height, (left_x - green_width):(right_x + green_width)]
    mask = mask[0:height, (left_x):(right_x)]
    height, width = mask.shape[0], mask.shape[1]
    for i in range(height):
        a = mask.copy()[i:(i+1), 0:width]
        if a.max() > 0:
            top_y = i
            break
    print("Top Y found")
    green_height = bottom_y - top_y
    img = img[top_y:bottom_y, left_x:right_x]
    mask = mask[top_y:height, 0:width]
    print(bottom_y)
    print(top_y)
    print(left_x)
    print(right_x)
    return mask, img

im = load_image()
import timeit
start = timeit.default_timer()
mask, im2 = trigger_image(im)
mask2, im3 = locate_green(mask, im2)
print(timeit.default_timer() - start)
tf.keras.utils.save_img("C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/leaphy2/mask.jpeg", mask)
tf.keras.utils.save_img("C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/leaphy2/check.jpeg", mask2)
tf.keras.utils.save_img("C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/leaphy2/result.jpeg", im3)