from PIL import Image
import random
import os

def RandomBackground(width, height):
    segments = random.randint(2, 10)
    im = Image.new(mode="RGB", size=(width, height), color="white")
    for i in range(segments):
        for j in range(segments):
            pim = Image.new(mode="RGB", 
                            size=(int(width/segments), int(height/segments)), 
                            color=(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ))
            im.paste(pim, (int(i*(width/segments)), int(j*(height/segments))))
    return im