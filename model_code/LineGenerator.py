import numpy as np
import random
from PIL import Image, ImageDraw
import os

#define settings
Image_amount = 1
Image_width = 640
Image_height = 100
line_width = 5

def GenerateImages(destination, category):
    if os.path.isdir(destination) == False:
        os.mkdir(destination)
    if len(os.listdir(destination)) > 0:
        for item in os.listdir(destination):
            os.remove(f"{destination}/{item}")
    
    back_image = Image.new(mode="RGB", size=(Image_width, Image_height), color="white").convert("RGBA")
    for i in range(Image_amount):
        if category == 0:
            rect_x = random.randint(0, int((Image_width/3)-line_width))
        elif category == 1:
            rect_x = random.randint(int((Image_width/3)), int((Image_width/3*2)-line_width))
        elif category == 2:
            rect_x = random.randint(int((Image_width/3*2)), Image_width)
        b_image = back_image.copy()
        draw = ImageDraw.Draw(b_image)
        draw.rectangle([rect_x, 10, rect_x+line_width, Image_height-10], fill="black")
        b_image = b_image.convert("RGB")
        b_image.save(f"{destination}/{i}.jpg")

def main():
    for i in [0, 1, 2]:
        GenerateImages(f"C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/destination/{i}", i)

if __name__ == "__main__":
    main()