from picamera2 import Picamera2
import time
import os

folder_location = "" #input folder path
images = 0 #input image amount
time_gaps = 0

camera = PiCamera2()
camera.resolution(1920, 1080)

def main():
    print("Starting")
    #check for valid save location
    if os.path.isdir(folder_location) == False:
        os.mkdir(folder_location)
        print(f"New folder created at {folder_location}")
    
    #start gathering
    camera.start_preview()
    for i in range(images):
        if (i+1) % 10 == 0 and i != 0:
            print(f"{i+1} images taken")
        camera.capture(f"{folder_location}/{i}.png")
        time.sleep(time_gaps)
    camera.stop_preview()

    if len(os.listdir(folder_location)) == images:
        print("Data gathering succesful")
    else:
        print(f"{images} images expected, {len(os.listdir(folder_location))} images taken")

if __name__ == "__main__":
    main()