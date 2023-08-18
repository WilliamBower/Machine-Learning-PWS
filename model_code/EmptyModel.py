import tensorflow as tf

def main():
    #create the model for training/saving
    model = create_model()
    
    #save the model
    save_path = "C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/model4" #define save location here
    tf.saved_model.save(model, save_path)

def create_model():
    #define model architecture
    inputs = tf.keras.Input(shape=(60, 60, 3))
    x = tf.keras.layers.Conv2D(32, (3,3), activation="relu")(inputs)
    x = tf.keras.layers.MaxPooling2D((2,2))(x)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(900, activation="relu")(x)
    x = tf.keras.layers.Dense(600, activation="softplus")(x)
    x = tf.keras.layers.Dense(300, activation="relu")(x)
    x = tf.keras.layers.Dense(100, activation="relu")(x)
    outputs = tf.keras.layers.Dense(40, activation="relu")(x)
    
    #create model
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    del inputs, outputs, x

    return model

if __name__ == "__main__":
    main()
