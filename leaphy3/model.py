import numpy as np
import tensorflow as tf
from PIL import Image

trigger_range_x = 0
trigger_range_y = 0
trigger_range_width = 1920
trigger_range_height = 1080

lower_colour = np.array([74, 9, 5])
higher_colour = np.array([159, 49, 24])

interpreter = tf.lite.Interpreter(model_path="")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()

model_width = 100
model_height = 100

labels = {
    0: "Stop",
    1: "50",
    2: "100"
}

def crop_and_mask(img):
    img = img[trigger_range_y:(trigger_range_y+trigger_range_height), trigger_range_x:(trigger_range_x+trigger_range_width)]
    img2 = np.all((img >= lower_colour) & (img <= higher_colour))
    mask = np.zeros_like(img)
    mask[img2] = img[img2]
    mask *= 255
    return img, mask

def locate_sign(img, mask):
    width, height = mask.shape[1], mask.shape[0]

    for i in range(height):
        a = mask.copy()[(height-i-1):(height-i), 0:width]
        if a.max() > 0:
            bottom_y = height-i
            break
    
    mask = mask[0:bottom_y, 0:width]
    height = mask.shape[0]
    for i in range(height):
        a = mask.copy()[i:(i+1), 0:width]
        if a.max() > 0:
            top_y = i
            break
    
    mask = mask[top_y:height, 0:width]
    height = mask.shape[0]
    for i in range(width):
        a = mask.copy()[0:height, i:(i+1)]
        if a.max() > 0:
            left_x = i
            break
    
    for i in range(width):
        a = mask.copy()[0:height, (width-i-1):(width-i)]
        if a.max() > 0:
            right_x = width-i
            break

    mask = mask[0:height, left_x:right_x]
    width = mask.shape[1]
    img = img[top_y:bottom_y, left_x:right_x]
    if width > height:
        img = img[0:height, ((width/2)-(height/2)):((width/2)+(height/2))]
    elif height > width:
        img = img[((height/2)-(width/2)):((height/2)+(width/2)), 0:width]
    return img, mask

def execute_model(img3):
    img = Image.fromarray(img)
    img = img.resize((model_width, model_height))
    img = np.array(img)
    img = img.astype(np.float32)
    img = np.expand_dims(img, axis=0)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_details = interpreter.get_output_details()
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]
    predictions = np.array(predictions)

    prediction = int(np.argwhere(predictions == max(predictions)))

    return predictions, prediction

def main(img=0):
    if img==0:
        return None
    img2, mask = crop_and_mask(img)
    if mask.max() > 0:
        img3, mask2 = locate_sign(img2, mask)
        model_results, predictions = execute_model(img3)
        return model_results, predictions

if __name__ == "__main__":
    main()