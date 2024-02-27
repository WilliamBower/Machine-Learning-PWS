import numpy as np
import tensorflow as tf
from PIL import Image

#Dit zijn libraries die op de Raspberry Pi staan
from picamera2 import Picamera2
from gpiozero import Motor

#Crop instellingen
trigger_range_x = 0
trigger_range_y = 500
trigger_range_height = 540
trigger_range_width = 1920

#Mask instellingen
lower_colour = np.array([74, 9, 5])
higher_colour = np.array([159, 49, 24])

#Model setup
interpreter = tf.lite.Interpreter(model_path="model1.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
IMG_WIDTH = 100
IMG_HEIGHT = 100
labels = {
    0: "Stop",
    1: "50",
    2: "100"
}

#Camera setup
camera = Picamera2()
cam_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (64, 64)})
camera.configure(cam_config)
camera.start_preview()
camera.start()

#Robot setup
class Leaphy():
    def __init__(self):
        self.motorL = Motor(27, 22)
        self.motorR = Motor(24, 23)
    def straight(self, speed):
        self.motorL.forward(speed)
        self.motorR.forward(speed)

leaphy = Leaphy()

def load_image():
    #Afbeelding inladen en correct formatten
    img = tf.io.read_file("input_image.jpg")
    img = tf.image.decode_jpeg(img)
    img = tf.image.rot90(img, k=2) #Afbeelding 180 graden draaien want camera zit op de kop
    img = np.array(img)
    img = img[:, :, :3] #Afbeelding formatten want heeft de shape (1080, 1920, 4) maar moet (1080, 1920, 3) zijn
    return img

def trigger_image(img):
    #Afbeelding croppen
    img = img[trigger_range_y:(trigger_range_y+trigger_range_height), trigger_range_x:(trigger_range_x+trigger_range_width)]

    img2 = np.all((img >= lower_colour) & (img <= higher_colour), axis=-1) #Alle pixels nemen binnen mask instellingen
    result = np.zeros_like(img) #Zwarte achtergrond maken
    result[img2] = img[img2] #Pixels van mask op zwarte achtergrond zetten
    result = result*255 #Alle pixels die niet in de achtergrond zitten wit maken
    #(heeft niet echt iets te maken met performance maar maakt debuggen makkelijker doordat de pixels duidelijk te zien zijn)
    return result, img

def locate_colour(mask, img):
    #Deze functie wordt alleen aangezet als er pixels in de mask zitten
    height, width = mask.shape[0], mask.shape[1]
    bottom_y = 0
    top_y = 0
    left_x = 0
    right_x = 0

    #Van onder naar boven scannen voor pixels die niet zwart zijn
    for i in range(height):
        a = mask.copy()[(height-i-1):(height-i), 0:width]
        if a.max() > 0:
            bottom_y = height - i
            break

    #Van boven naar onder scannen voor pixels die niet zwart zijn
    mask = mask[0:bottom_y, 0:width]
    height, width = mask.shape[0], mask.shape[1]
    for i in range(height):
        a = mask.copy()[i:(i+1), 0:width]
        if a.max() > 0:
            top_y = i
            break
    
    #Van links naar rechts scannen voor pixels die niet zwart zijn
    mask = mask[top_y:height, 0:width]
    height, width = mask.shape[0], mask.shape[1]
    for i in range(width):
        a = mask.copy()[0:height, i:(i+1)]
        if a.max() > 0:
            left_x = i
            break
    
    #Van rechts naar links scannen voor pixels die niet zwart zijn
    #Deze loop zou kunnen worden vervangen om altijd perfect vierkanten te krijgen, met risico dat het model belangrijke data niet krijgt
    for i in range(width):
        a = mask.copy()[0:height, (width-i-1):(width-i)]
        if a.max() > 0:
            right_x = width - i
            break
    mask = mask[0:height, left_x:right_x]
    height, width = mask.shape[0], mask.shape[1]
    img = img[top_y:bottom_y, (left_x-(width*0)):(right_x+(width*0))]
    return mask, img

def execute_model(im):
    #Afbeelding formatten voor gebruik in het model
    im = Image.fromarray(im)
    im = im.resize((IMG_WIDTH, IMG_HEIGHT))
    im = np.array(im)
    im = im.astype(np.float32)
    im = np.expand_dims(im, axis=0)

    #Model uitvoeren
    interpreter.set_tensor(input_details[0]['index'], im)
    interpreter.invoke()
    output_details = interpreter.get_output_details()
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]
    predictions = np.array(predictions)
    return predictions

def main():
    leaphy.straight(0.2)
    while True:
        camera.capture_file("input_image.jpg")
        im = load_image()
        mask, im2 = trigger_image(im)
        n = mask.max()
        if n > 0:
            #Afbeelding croppen voor het model
            mask2, im3 = locate_colour(mask, im2)
            #Model uitvoeren
            model_result = execute_model(im3)

            #Motoren aansturen
            if int(np.argwhere(model_result == max(model_result))) == 0:
                leaphy.straight(0)
                print(0)
            elif int(np.argwhere(model_result == max(model_result))) == 1:
                leaphy.straight(0.2)
                print(1)
            else:
                leaphy.straight(0.2)
                print(2)
            if int(np.argwhere(model_result == max(model_result))) == 1:
                break

            #Model resultaten printen
            new_page = '\n'*60
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
