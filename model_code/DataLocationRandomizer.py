import numpy as np
import random
from PIL import Image
import os
import BackgroundRandomizer

#define settings
Image_amount = 100
Image_width = 1920
Image_height = 1080

def GenerateImages(destination, base, randomized=False):
    if os.path.isdir(destination) == False:
        os.mkdir(destination)
    #delete files in destination directory for ease of use and 
    if len(os.listdir(destination)) > 0:
        for item in os.listdir(destination):
            os.remove(f"{destination}/{item}")

    #load images
    front_image = Image.open(base).convert("RGBA")
    fi_width, fi_height = front_image.size

    for i in range(Image_amount):
        #create background image
        if randomized == False:
            back_image = Image.new(mode="RGB", size=(Image_width, Image_height), color="white").convert("RGBA")
        else:
            back_image = BackgroundRandomizer.RandomBackground(Image_width, Image_height)
        bi_width, bi_height = back_image.size

        #randomize the size of the front image
        im_width = im_height = random.randint((fi_height/10), bi_height)
        im = front_image.resize((im_width, im_height))
        
        max_x = bi_width - (im_width)
        max_y = bi_height - (im_height)

        #check for valid image size
        if max_x < 0 or max_y < 0:
            print("Invalid image size for placement")
            continue

        #randomize the location of the image
        im_x = random.randint(0, max_x)
        im_y = random.randint(0, max_y)

        #merge images together and save
        b_image = back_image.copy()
        b_image.paste(im, (im_x, im_y), im)
        b_image = b_image.convert("RGB")
        b_image.save(f"{destination}/{i}.jpg")

        #give updates to user
        if (i+1)%5 == 0:
            print(f"{i+1} images created")
    print("All images generated\n")

def main():
    #define the path of where the images are being saved
    Image_save_location = "C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/image_destination"
    if os.path.isdir(Image_save_location):
        os.mkdir(Image_save_location)
        print("Base directory made")
    #define the images that are being pasted on the background
    base_locations = [
        "C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/base_images/50.jpg",
        "C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/base_images/100.jpg"
    ]

    #generate the images
    for i in range(len(base_locations)):
        GenerateImages(f"{Image_save_location}/{i}", base_locations[i], randomized=True)

    dest = "C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/image_destination"
    print("\nImages per folder:")
    for folder in os.listdir(dest):
        length = len(os.listdir(f"{dest}/{folder}"))
        print(f"{folder}: {length}")
        print("--------------------")

if __name__ == "__main__":
    main()