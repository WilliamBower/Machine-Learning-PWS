import numpy as np
import tensorflow as tf
from picamera2 import Picamera2

trigger_range_x = 0
trigger_range_y = 0
trigger_range_height = 540
trigger_range_width = 1920
lower_colour = np.array([225, 9, 21])
higher_colour = np.array([227, 11, 23])
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
IMG_WIDTH = 100
IMG_HEIGHT = 100
camera = Picamera2()
cam_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (64, 64)})
camera.configure(cam_config)
camera.start_preview()
camera.start()

labels = {
    0: "plus",
    1: "min"
}

def load_image():
    img = tf.io.read_file("input_image.jpg")
    img = tf.image.decode_jpeg(img)
    img = tf.image.rot90(img, k=2)
    img = np.array(img)
    img = img[:, :, :3]
    print(img.shape)
    return img

def trigger_image(img):
    print("Creating Mask")
    img = img[trigger_range_y:(trigger_range_y+trigger_range_height), trigger_range_x:(trigger_range_x+trigger_range_width)]
    img2 = np.all((img >= lower_colour) & (img <= higher_colour), axis=-1)
    result = np.zeros_like(img)
    result[img2] = img[img2]
    print("Mask created")
    return result, img

def locate_colour(mask, img):
    print("Locating")
    height, width = mask.shape[0], mask.shape[1]
    bottom_y = 0
    top_y = 0
    left_x = 0
    right_x = 0

    for i in range(height):
        a = mask.copy()[(height-i-1):(height-i), 0:width]
        if a.max() > 0:
            bottom_y = height - i
            break
    print("Bottom Y found")

    mask = mask[0:bottom_y, 0:width]
    height, width = mask.shape[0], mask.shape[1]
    for i in range(height):
        a = mask.copy()[i:(i+1), 0:width]
        if a.max() > 0:
            top_y = i
            break
    print("Top Y found")

    mask = mask[top_y:height, 0:width]
    height, width = mask.shape[0], mask.shape[1]
    for i in range(width):
        a = mask.copy()[0:height, i:(i+1)]
        if a.max() > 0:
            left_x = i
            break
    print("Left X found")

    right_x = left_x + height
    mask = mask[0:height, left_x:right_x]
    img = img[top_y:bottom_y, left_x:right_x]
    print(bottom_y)
    print(top_y)
    print(left_x)
    print(right_x)
    return mask, img

def execute_model(im):
    im = im.reshape(IMG_WIDTH, IMG_HEIGHT, 3)
    interpreter.set_tensor(input_details[0]['index'], im)
    interpreter.invoke()
    output_details = interpreter.get_output_details()
    predictions = interpreter.get_tensor(output_details[0]['index'][0])

def main():
    while True:
        camera.capture_file("input_image.jpg")
        im = load_image()
        mask, im2 = trigger_image(im)
        n = mask.max()
        if n != 0:
            mask, im2 = trigger_image(im)
            mask2, im3 = locate_colour(mask, im2)
            model_result = execute_model(im3)
            print(""*30)
            print("Voorspelling:")
            print(labels[model_result.index(model_result.max())])
            print()
            for value, index in enumerate(model_result):
                print(f"{labels[index]} | {value}")

if __name__ == "__main__":
    main()