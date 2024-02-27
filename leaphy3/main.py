import time
import tensorflow as tf
import numpy as np
from threading import Thread
from queue import Queue

"""
from picamera2 import Picamera2
from gpiozero import Motor

camera = Picamera2()
cam_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (64, 64)})
camera.configure(cam_config)
camera.start_preview()
camera.start()

class Leaphy():
    def __init__(self):
        self.motorL = Motor(27, 22)
        self.motorR = Motor(24, 23)

    def straight(self, l_speed, r_speed):
        if l_speed > 0:
            self.motorL.forward(l_speed)
        elif l_speed < 0:
            self.motorL.backward(abs(l_speed))
        else:
            self.motorL.stop()
        
        if r_speed > 0:
            self.motorR.forward(r_speed)
        elif r_speed < 0:
            self.motorR.backward(abs(r_speed))
        else:
            self.motorR.stop()

#leaphy = Leaphy()
"""
line_interval = 1
model_interval = 5

l_speed = 0.1
r_speed = 0.1
max_l_speed = 0.5
max_r_speed = 0.5
scaling_1 = 0.1
scaling_2 = 0.4


def take_image():
    camera.capture_file("input_image.jpg")
    img = tf.io.read_file("input_image.jpg")
    img = tf.image.rot90(img, k=2)
    img = np.array(img)
    img = img[:, :, :3]
    return img

def line_thread(queue):
    print(1)
    #line.main()
    last_time = time.time()
    queue.put(last_time)

def model_thread(queue):
    print(2)
    #model.main()
    last_time = time.time()
    queue.put(last_time)

def main():
    last_line_time = time.time()
    last_model_time = time.time()
    result_queue_line = Queue()
    result_queue_model = Queue()

    while True:
        #img = take_image()
        if time.time() - last_line_time >= line_interval:
            t1 = Thread(target=line_thread, args=(result_queue_line, ))
            t1.start()
            
        if time.time() - last_model_time >= model_interval:
            t2 = Thread(target=model_thread, args=(result_queue_model, ))
            t2.start()
        
        while not result_queue_line.empty():
            last_line_time = result_queue_line.get()
        
        while not result_queue_model.empty():
            last_model_time = result_queue_model.get()

if __name__ == "__main__":
    main()