paths = ["C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/test/image0.jpeg",
         "C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/test/image1.jpeg",
         "C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/test/image2.jpeg"]

#imports
import numpy as np
import tensorflow as tf
import timeit

threshold = 40

def find_line(img):
    start_time = timeit.timeit()

    #process input image
    img = tf.image.rgb_to_grayscale(img) 
    img = np.array(img)
    height, width = img.shape[0], img.shape[1]

    #split image
    first_third = img.copy()[0:height, 0:(int(width/3))]
    second_third = img.copy()[0:height, (int(width/3)):(int(width/3*2))]
    third_third = img.copy()[0:height, (int(width/3*2)):width]

    #find black pixels (pixels with value below threshold)
    a = np.sum(first_third<=threshold)
    b = np.sum(second_third<=threshold)
    c = np.sum(third_third<=threshold)

    #get measurements
    results = (a, b, c)
    end_time = timeit.timeit()

    movements = {
        0: "Left",
        1: "Straight",
        2: "Right"
    }
    #give outputs
    print(f"Results = {results}")
    print(f"Highest = {max(results)}")
    print(f"Turn {movements[(results).index(max(results))]}")
    print(f"Time = {end_time - start_time}")

def format_image(path, save=True):
    #read images
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img)
    img = np.array(img)
    
    #get images properties
    height, width = img.shape[0], img.shape[1]

    #crop image
    img = img[1957:height, (int(width/4)):(int(width/4*3))]

    #save if applicable
    if save==True:
        tf.keras.utils.save_img("0.jpg", img)   
        return
    else:
        return img

def main():
    #run program for every image given
    for path in paths:
        find_line(format_image(path, False))
        print()

if __name__ == "__main__":
    main()