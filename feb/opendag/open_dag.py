import numpy as np
import tensorflow as tf
from picamera2 import Picamera2
from PIL import Image
import RPi.GPIO as GPIO
from gpiozero import Motor

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#red_pin = 12
#green_pin = 19
#blue_pin = 13
#GPIO.setup(red_pin, GPIO.OUT)
#GPIO.setup(green_pin, GPIO.OUT)
#GPIO.setup(blue_pin, GPIO.OUT)
#GPIO.output(red_pin, GPIO.LOW)
#GPIO.output(green_pin, GPIO.LOW)
#GPIO.output(blue_pin, GPIO.LOW)
trigger_range_x = 0
trigger_range_y = 500
trigger_range_height = 540
trigger_range_width = 1920
lower_colour = np.array([74, 9, 5])
#149, 86, 94
higher_colour = np.array([159, 49, 24])
#201, 134, 151
interpreter = tf.lite.Interpreter(model_path="model1.tflite")
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
    0: "Stop",
    1: "50",
    2: "100"
}

class Leaphy():
    def __init__(self):
        self.motorL = Motor(27, 22)
        self.motorR = Motor(24, 23)
    def straight(self, speed):
        self.motorL.forward(speed)
        self.motorR.forward(speed)

leaphy = Leaphy()

def load_image():
    img = tf.io.read_file("input_image.jpg")
    img = tf.image.decode_jpeg(img)
    img = tf.image.rot90(img, k=2)
    img = np.array(img)
    img = img[:, :, :3]
#    print(img.shape)
    return img

def trigger_image(img):
#    print("Creating Mask")
    img = img[trigger_range_y:(trigger_range_y+trigger_range_height), trigger_range_x:(trigger_range_x+trigger_range_width)]
    img2 = np.all((img >= lower_colour) & (img <= higher_colour), axis=-1)
    result = np.zeros_like(img)
    result[img2] = img[img2]
    result = result*255
#    print("Mask created")
    return result, img

def locate_colour(mask, img):
#    print("Locating")
    height, width = mask.shape[0], mask.shape[1]
    bottom_y = 0
    top_y = 0
    left_x = 0
    right_x = 0

    for i in range(height):
        a = mask.copy()[(height-i-1):(height-i), 0:width]
#        print(a.max())
        if a.max() > 50:
#            print("Break")
            bottom_y = height - i
            break
#    print("Bottom Y found")

    mask = mask[0:bottom_y, 0:width]
    height, width = mask.shape[0], mask.shape[1]
    for i in range(height):
        a = mask.copy()[i:(i+1), 0:width]
 #       print(a.max())
        if a.max() > 50:
 #           print("Break")
            top_y = i
            break
 #   print("Top Y found")

    mask = mask[top_y:height, 0:width]
    height, width = mask.shape[0], mask.shape[1]
    for i in range(width):
        a = mask.copy()[0:height, i:(i+1)]
  #      print(a.max())
        if a.max() > 50:
  #          print("Break")
            left_x = i
            break
#    print("Left X found")

    for i in range(width):
        a = mask.copy()[0:height, (width-i-1):(width-i)]
        if a.max() > 50:
            right_x = width - i
            break
#    right_x = left_x + height
    mask = mask[0:height, left_x:right_x]
    height, width = mask.shape[0], mask.shape[1]
    img = img[top_y:bottom_y, (left_x-(width*0)):(right_x+(width*0))]
 #   print(bottom_y)
 #   print(top_y)
 #   print(left_x)
 #   print(right_x)
    return mask, img

def execute_model(im):
    im = Image.fromarray(im)
    im = im.resize((IMG_WIDTH, IMG_HEIGHT))
    im = np.array(im)
    im = im.astype(np.float32)
    im = np.expand_dims(im, axis=0)
 #   print(im.shape)
    interpreter.set_tensor(input_details[0]['index'], im)
    interpreter.invoke()
    output_details = interpreter.get_output_details()
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]
    predictions = np.array(predictions)
#    print("Pred")
#    print(predictions)
#    print()
    return predictions

def main():
    leaphy.straight(0.2)
    while True:
        camera.capture_file("input_image.jpg")
        im = load_image()
        mask, im2 = trigger_image(im)
        mask = np.dot(mask[...,:3], [0.2989, 0.5870, 0.1140])
        n = mask.max()
#        print(n)
        if n != 0:
#            mask, im2 = trigger_image(im)
#            tf.keras.utils.save_img("mask.jpg", mask)
            mask2, im3 = locate_colour(mask, im2)
            tf.keras.utils.save_img("crop.jpg", im3)
            model_result = execute_model(im3)
#            model_result = [0, 1]
 #           print(im3.shape)
            if int(np.argwhere(model_result == max(model_result))) == 0:
                leaphy.straight(0)
                print(0)
            elif int(np.argwhere(model_result == max(model_result))) == 1:
                leaphy.straight(0.2)
                print(1)
            else:
                leaphy.straight(0.2)
                print(2)
            im4 = Image.fromarray(im3)
            im4 = im4.resize((IMG_WIDTH, IMG_HEIGHT))
            im4 = np.array(im4)
            im4 = im4.astype(np.float32)
            im4 = np.expand_dims(im4, axis=0)
            im4 = np.squeeze(im4)
 #           print(im4.shape)
            mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
            tf.keras.utils.save_img("mask.jpg", mask)
            tf.keras.utils.save_img("model.jpg", im4)
            if int(np.argwhere(model_result == max(model_result))) == 1:
                break
            new_page = '\n'*1
            new_line = '\n'
            result_name = labels[int(np.argwhere(model_result == max(model_result)))]
            probs = ""
            for index, value in enumerate(model_result):
                probs = probs + '\n' + f"{labels[index]} | {value}"
            print(f"{new_page}{probs}{new_line}{new_line}Voorspelling:{new_line}{result_name}")
            print(im3.shape)
        else:
            print("\n"*60)
            print("Geen Voorwerp")
if __name__ == "__main__":
    main()
