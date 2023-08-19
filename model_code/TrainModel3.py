import tensorflow as tf
print("Tensorflow version: ", tf.__version__)
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras import Model
import numpy as np
import sys
import os
from sklearn.model_selection import train_test_split

IMG_WIDTH = 30
IMG_HEIGHT = 30
EPOCHS = 16
NUM_CATEGORIES = 2
TEST_SIZE = 0.4

def main():
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python TrainedModel.py data_directory [model.h5]")

    images = []
    labels = []

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

    model = train_model(x_train, x_test, y_train, y_test)

    if len(sys.argv) == 2:
        model.save(sys.argv[2])
        print("saved")
    print(model.summary())

class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = Conv2D(32, (3,3), activation="relu")
        self.maxpool = MaxPooling2D(pool_size=(2,2))
        self.flatten = Flatten()
        self.l1 = Dense(900, activation="relu")
        self.l2 = Dense(600, activation="softplus")
        self.l3 = Dense(300, activation="relu")
        self.l4 = Dense(100, activation="relu")
        self.l5 = Dense(NUM_CATEGORIES, activation="softmax")

    def call(self, x):
        x = self.conv1(x)
        x = self.maxpool(x)
        x = self.flatten(x)
        x = self.l1(x)
        x = self.l2(x)
        x = self.l3(x)
        x = self.l4(x)
        return self.l5(x)

def load_image(path):
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image)
    image = tf.image.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    image_array = image.numpy()
    image_array = image_array.reshape(1, IMG_WIDTH, IMG_HEIGHT, 3)
    return image_array

def train_model(x_train, x_test, y_train, y_test):
    model = MyModel()
    loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    optimizer = tf.keras.optimiziers.Adam()
    train_loss = tf.keras.metrics.Mean(name="train_loss")
    train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name="train_accuracy")
    test_loss = tf.keras.metrics.Mean(name="test_loss")
    test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name="test_accuracy")

    @tf.function
    def train_step(images, labels):
        with tf.GradientTape() as tape:
            predictions = model(images, training=True)
            loss = loss_object(labels, predictions)
        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        train_loss(loss)
        train_accuracy(labels, predictions)

    @tf.function
    def test_step(images, labels):
        predictions = model(images, training=False)
        t_loss = loss_object(labels, predictions)

        test_loss(t_loss)
        test_accuracy(labels, predictions)
    
    for epoch in range(EPOCHS):
        train_loss.reset_states()
        train_accuracy.reset_states()
        test_loss.reset_states()
        test_accuracy.reset_states()

        for images, labels in x_train, y_train:
            train_step(images, labels)
        
        for test_images, test_labels in (x_test, y_test):
            test_step(test_images, test_labels)
        
        print(
            f"Epoch {epoch + 1}, "
            f"Loss: {train_loss.result()}, "
            f"Accuracy: {train_accuracy.result() * 100}, "
            f"Test Loss: {test_loss.result()}, "
            f"Test Accuracy: {test_accuracy.result() * 100}"
        )
    
    return model

if __name__ == "__main__":
    main()