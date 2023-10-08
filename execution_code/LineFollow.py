from picamera2 import Picamera2
import os
import tensorflow as tf
import numpy as np
import time

movements = {
    0: "Left",
    1: "Straight",
    2: "Right"
}
threshold = 40
wait_time = 0.1

def follow_line():
    camera = Picamera2()
    cam_config = camera.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (64, 64)})
    camera.configure(cam_config)
    start_time = 0
    camera.start_preview()
    camera.start()
    iteration = 0
    while True:
        time.sleep(start_time + wait_time - time.time())
        start_time = time.time()
        camera.capture_file("image.jpg")
        
        img = tf.io.read_file("image.jpg")
        img = tf.image.decode_jpeg(img)
        img = np.array(img)

        height, width = img.shape[0], img.shape[1]
        img = img[(int(height*0.9)):height, (int(width/4)):(int(width/4*3))]
        results = find_line(img)
        instruction = movements[(results.index(max(results)))]
        print(f"Turn: {instruction}")
        iteration += 1
        if iteration == 100:
            break

def find_line(img):
    img = tf.image.rgb_to_grayscale(img)
    img = np.array(img)
    height, width = img.shape[0], img.shape[1]

    first_third = img.copy()[0:height, 0:(int(width/3))]
    second_third = img.copy()[0:height, (int(width/3)):(int(width/3*2))]
    third_third = img.copy()[0:height, (int(width/3*2)):width]

    a = np.sum(first_third<=threshold)
    b = np.sum(second_third<=threshold)
    c = np.sum(third_third<=threshold)
    results = (a, b, c)

    return results

def main():
    follow_line()

if __name__ == "__main__":
    main()