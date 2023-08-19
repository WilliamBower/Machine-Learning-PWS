from picamera2 import Picamera2
import sys

if len(sys.argv) not in [2, 3]:
    sys.exit("Usage: python TrainedModel.py data_directory [model.h5]")

IMG_WIDTH = 1920
IMG_HEIGHT = 1080

camera = Picamera2()
cam_config = camera.create_still_configuration(main={"size": (IMG_WIDTH, IMG_HEIGHT)}, lores={"size": (30, 30)})
camera.configure(cam_config)
camera.start_preview()
camera.start()
camera.capture_file(sys.argv[1])
camera.stop_preview()