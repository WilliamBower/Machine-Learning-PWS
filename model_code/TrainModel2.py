import os
import sys
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

IMG_WIDTH = 30
IMG_HEIGHT = 30
EPOCHS = 16
NUM_CATEGORIES = 2
TEST_SIZE = 0.4

def main():
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python TrainedModel.py data_directory save_location [model.h5]")

    images = []
    labels = []

    #Loading images into memory
    for folder in os.listdir(sys.argv[1]):
        print(folder)
        if os.path.isdir(f"{sys.argv[1]}/{folder}"):
            print(True)
            for files in os.listdir(f"{sys.argv[1]}/{folder}"):
                print(files)
                images.append(load_image(f"{sys.argv[1]}/{folder}/{files}"))
                labels.append(folder)

    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    model = create_model()

    model.fit(x_train, y_train, epochs=EPOCHS)

    model.evaluate(x_test, y_test, verbose=2)

    if len(sys.argv) == 2:
        model.save(sys.argv[2])


def load_image(path):
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image)
    image = tf.image.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    image_array = image.numpy()
    image_array = image_array.reshape(1, IMG_WIDTH, IMG_HEIGHT, 3)
    return image_array

def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)
        ),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(900, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(600, activation="softplus"),
        tf.keras.layers.Dense(300, activation="relu"),
        tf.keras.layers.Dense(100, activation="relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])
    
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    main()