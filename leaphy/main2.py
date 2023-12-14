#import image_operations, line_find, motor_operations, model_operations
import math, copy, json
from datetime import datetime, timedelta
from threading import Thread
import tensorflow as tf

line_split = 5
if (line_split % 2) == 0:
    line_split += 1
middle_line = math.floor(line_split/2)

model_image_compression = 10
last_model_prediction = None

line_interval = 0.1
model_interval = 1

current_speed = 1
motor_active = True

demo_active = False
demo_path = "demo"

line_output = []
model_output = []

def capture_image():
    image_operations.picture()
    img = image_operations.load_image
    return img

def locate_line(img):
    line_img = image_operations.line_image(img, line_split)
    line_result = line_find.locate_line(line_img, line_split)
    line_output = line_result
    return line_result

def run_model(img):
    model_img = image_operations.model_image(img, model_image_compression)
    model_result = model_operations.execute_model(model_img)
    model_output = model_result
    return model_result

def line_thread(img):
    line_result = locate_line(img)

    if line_result == middle_line and motor_active:
        motor_operations.leaphy.straight(current_speed)
    elif line_result < middle_line and motor_active:
        perc = 1/(line_result+1)
        motor_operations.leaphy.l_turn(perc, current_speed)
    elif line_result > middle_line and motor_active:
        perc = 1/(line_split-line_result)
        motor_operations.leaphy.r_turn(perc, current_speed)

def model_thread(img):
    model_result = run_model(img)

def demo_thread(img, time):
    result_dict = {
        "time": datetime.now(),
        "line": line_output,
        "model": model_output
    }
    with open(f"{demo_path}/results.json", "r") as f:
        file = json.load(f)
    file.append(result_dict)
    tf.keras.utils.save_img(f"{demo_path}/{time.strftime('%H:%M:%S:%f')}.png", img)
    with open(f"{demo_path}/results.json", "w") as f:
        f.write(json.dumps(file, indent=4))

def main():
    last_line_time = datetime.now()
    last_model_time = datetime.now()
    if demo_active:
        with open(f"{demo_path}/results.json", "w") as f:
            f.write(json.dumps([], indent=4))
    while True:
        a = datetime.now()
        img = capture_image()
        if (round(int(a.strftime("%f")), -5) >= 
            round(int((last_line_time + timedelta(seconds=line_interval)).strftime("%f")), -5)
            ) and (
            int(a.strftime("%S")) >=
            int((last_line_time + timedelta(seconds=line_interval)).strftime("%S"))
        ):
            last_line_time = copy.copy(a)
            t1 = Thread(target=line_thread, args=(img,))
            t1.start()

        if (round(int(a.strftime("%f")), -5) >= 
            round(int((last_model_time + timedelta(seconds=model_interval)).strftime("%f")), -5)
            ) and (
            int(a.strftime("%S")) >=
            int((last_model_time + timedelta(seconds = model_interval)).strftime("%S"))
        ):
            last_model_time = copy.copy(a)
            t2 = Thread(target=model_thread, args=(img,))
            t2.start()
        if demo_active:
            t3 = Thread(target=demo_thread, args=(img,a,))
            t3.start()

if __name__ == "__main__":
    main()