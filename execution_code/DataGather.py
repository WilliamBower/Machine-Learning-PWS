from picamera2 import Picamera2
import time
import os
import sys

if len(sys.argv) not in [3, 4]:
    sys.exit("Usage: python TrainedModel.py data_directory [model.h5]")

folder_location = sys.argv[1]
if os.path.isdir(folder_location) == False:
    os.mkdir(folder_location)
    print(f"New folder created at {folder_location}")
images = sys.argv[2]
time_gaps = 0
IMG_WIDTH = 1920
IMG_HEIGHT = 1080

camera = Picamera2()
cam_config = camera.create_still_configuration(main={"size": (IMG_WIDTH, IMG_HEIGHT)}, lores={"size": (30, 30)})
camera.configure(cam_config)

def main():
    print("Starting")
    camera.start_preview()
    camera.start()
    import timeit
    start_time = timeit.default_timer()
    for i in range(images):
        if (i+1) % 10 == 0 and i != 0:
            print(f"{i+1} images taken")
        camera.capture_file(f"{folder_location}/{i}.jpg")
        time.sleep(time_gaps)
    end_time = timeit.default_timer()
    camera.stop_preview()
    print(f"Time duration: {end_time - start_time}")

    if len(os.listdir(folder_location)) == images:
        print("Data gathering succesful")
    else:
        print(f"{images} images expected, {len(os.listdir(folder_location))} images taken")

if __name__ == "__main__":
    main()