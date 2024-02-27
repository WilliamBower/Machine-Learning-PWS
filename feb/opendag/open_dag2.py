import numpy as np
import tensorflow as tf
from picamera2 import Picamera2
from PIL import Image

trigger_range_x = 0
trigger_range_y = 540
trigger_range_height = 540
trigger_range_width = 1920
lower_colour = np.array([45, 10, 6])
#149, 86, 94
higher_colour = np.array([58, 15, 9])
#201, 134, 151
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
    0: "Corderius College",
    1: "Plus",
    2: "Min",
    3: "Keer",
    4: "Delen",
    5: "Kwadraat",
    6: "Wortel"
}

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
#    print(result.shape)
#    result = np.expand_dims(result, axis=2)
#    print(result.shape)
    result = Image.fromarray(result)
    result = result.convert("L")
    result = np.array(result)
    result = result*255
#    result = np.repeat(result[:, :, np.newaxis], 3, axis=2)
    print(result.shape)
#    print("Mask created")
    return result, img

def locate_colour(mask, img):
    print("Locating")
    height, width = mask.shape[0], mask.shape[1]
    bottom_y = 0
    top_y = 0
    left_x = 0
    right_x = 0
    print(width)

    left_side = img[0:height, 0:int((width/2))]
    right_side = img[0:height, int((width/2)):width]
    print(left_side.shape)
    print(right_side.shape)
    print(np.sum(left_side>0)/255)
    print(np.sum(right_side>0)/255)
    print(left_side.max())
    print(right_side.max())

def execute_model(im):
    im = Image.fromarray(im)
    im = im.resize((IMG_WIDTH, IMG_HEIGHT))
    im = np.array(im)
    im = im.astype(np.float32)
    im = np.expand_dims(im, axis=0)
    print(im.shape)
    interpreter.set_tensor(input_details[0]['index'], im)
    interpreter.invoke()
    output_details = interpreter.get_output_details()
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]
    predictions = np.array(predictions)
    print("Pred")
    print(predictions)
    print()
    return predictions

def main():
    while True:
        camera.capture_file("input_image.jpg")
        im = load_image()
        mask, im2 = trigger_image(im)
        print(mask[0])
        n = mask.max()
        print(n)
        if n != 0:
            mask, im2 = trigger_image(im)
 #           tf.keras.utils.save_img("mask.jpg", mask)
            mask2, im3 = locate_colour(mask, im2)
            tf.keras.utils.save_img("crop.jpg", im3)
            model_result = execute_model(im3)
#            model_result = [0, 1]
            print(im3.shape)
            im4 = Image.fromarray(im3)
            im4 = im4.resize((IMG_WIDTH, IMG_HEIGHT))
            im4 = np.array(im4)
            im4 = im4.astype(np.float32)
            im4 = np.expand_dims(im4, axis=0)
            im4 = np.squeeze(im4)
            mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
            print(im4.shape)
            tf.keras.utils.save_img("mask.jpg", mask)
            tf.keras.utils.save_img("model.jpg", im4)
            print("\n"*50)
            print("Voorspelling:")
            print(im3.shape)
            print(im4.shape)
            print(labels[int(np.argwhere(model_result == max(model_result)))])
            print()
            for index, value in enumerate(model_result):
                print(f"{labels[index]} | {value}")

if __name__ == "__main__":
    main()
