import tensorflow as tf

def main():
    raise NotImplementedError()

def load_image(path):
    raise NotImplementedError()

def load_model(path):
    return tf.saved_model.load(path)

def run_model(model, data):
    return model(data)

if __name__ == "__main__":
    main()
