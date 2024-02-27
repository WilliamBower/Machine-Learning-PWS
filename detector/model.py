import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
import os
import numpy as np
import json

directory = "C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/detector/model_data"
IMG_WIDTH = 96
IMG_HEIGHT = 108
TEST_SIZE = 0.4
EPOCHS = 100

def load_all_images(path):
    images = []
    labels = []
    #Loading images into memory
    for files in os.listdir(f"{path}"):
        #print(files)
        img, lab = load_image(f"{path}/{files}")
        images.append(img)
        labels.append(lab)

    print(labels)
    return images, labels

def load_image(path):
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image)
    image = tf.image.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    image_array = np.array(image)
    image_array = image_array.reshape(IMG_WIDTH, IMG_HEIGHT, 3)
    img_id = str(int(path[-8:-4]))
    #print(path)
    #print(img_id)
    #label = label_list[img_id]
    #label = np.array(label)
    #label = tf.convert_to_tensor(label, dtype=tf.float32)
    label = [100, 100, 200, 200]
    #label = tf.convert_to_tensor([100.0, 100.0, 200.0, 200.0])
    print(label)
    return image_array, label

with open("C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/detector/labels.json", "r") as f:
  label_list = json.load(f)
images, labels = load_all_images(directory)
images = images
labels = labels

num_val_samples = int(TEST_SIZE * len(images))
print(images)
x_train = images[num_val_samples:]
x_test = images[:num_val_samples]
y_train = labels[num_val_samples:]
y_test = images[:num_val_samples]

#print(len(y_train))

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(96, 108, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(4)
])

model.compile(optimizer="adam", loss="mean_squared_error")

early_stopping = EarlyStopping(monitor="val_loss",
                               patience=5,
                               verbose=1,
                               mode="min",
                               baseline=None,
                               restore_best_weights=True)

history = model.fit(x_train, y_train, epochs=EPOCHS,
                    validation_data=(x_test, y_test),
                    callbacks=[early_stopping],
                    batch_size=64)

model.evaluate(x_test, y_test, verbose=2)