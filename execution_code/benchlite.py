from tensorflow.keras.models import load_model
import tensorflow as tf
import os
import numpy as np

model_path = ""
data_path = ""
IMG_WIDTH = 96
IMG_HEIGHT = 108
test = 2

def load_image(path):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img)
    img = tf.image.resize(img, (IMG_WIDTH, IMG_HEIGHT))
    img_arr = img.numpy()
    img_arr = img_arr.reshape(IMG_WIDTH, IMG_HEIGHT, 3)
    img_arr = np.array(img_arr)[np.newaxis,...]
    return img_arr

def prediction(img, interpreter, input_details):
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_details = interpreter.get_output_details()
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]
    return predictions

def main():
    img = load_image(data_path)
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    import timeit
    from gpiozero import CPUTemperature
    cpu = CPUTemperature()
    temps = [cpu.temperature]
    start_time = timeit.default_timer()
    for i in range(100):
        prediction(img, interpreter, input_details)
        temps.append(cpu.temperature)
    end_time = timeit.default_timer()
    result_time = end_time - start_time
    avg_time = result_time / 100
    dtemp = temps[-1] - temps[0]
    import json
    data = {
        "cpu temperatures": temps,
        "delta temperature": dtemp,
        "average delta temperature": dtemp/100,
        "total time": result_time,
        "average time": avg_time
    }
    with open(f"test{test}.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    main()