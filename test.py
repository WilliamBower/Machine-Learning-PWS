paths = ["C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/test/image0.jpeg",
         "C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/test/image1.jpeg",
         "C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/test/image2.jpeg"]
import numpy as np
import tensorflow as tf

def find_black(img):
    import timeit
    start_time = timeit.timeit()

    #img = tf.io.read_file(path)
    #img = tf.image.decode_jpeg(img)
    #
    img = tf.image.rgb_to_grayscale(img)
    tf.keras.utils.save_img("0.jpg", img)  
    img = np.array(img)
    print(img.shape[0])
    height, width = img.shape[0], img.shape[1]
    print(width)
    print(height)

    first_third = img.copy()[0:height, 0:(int(width/3))]
    second_third = img.copy()[0:height, (int(width/3)):(int(width/3*2))]
    third_third = img.copy()[0:height, (int(width/3*2)):width]

    a = np.sum(first_third<=50)
    b = np.sum(second_third<=50)
    c = np.sum(third_third<=50)

    end_time = timeit.timeit()

    print(a)
    print(b)
    print(c)
    print(f"Highest = {max(a, b, c)}")
    movements = {
        0: "Right",
        1: "Straight",
        2: "Left"
    }
    print(f"Turn {movements[(a, b, c).index(max(a, b, c))]}")
    print(end_time - start_time)

def format_image(path, save=True):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img)
    img = np.array(img)
    height, width = img.shape[0], img.shape[1]
    img = img[1957:height, (int(width/4)):(int(width/4*3))]
    if save==True:
        tf.keras.utils.save_img("0.jpg", img)   
        return
    else:
        return img

def main():
    for path in paths:
        img = format_image(path, False)
        find_black(img)
        print()
        break

if __name__ == "__main__":
    main()