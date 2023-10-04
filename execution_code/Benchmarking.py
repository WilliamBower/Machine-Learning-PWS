import tensorflow as tf

IMG_WIDTH = 1920
IMG_HEIGHT = 1080
iterations = 100
test = 1
def main():
    image = load_image("resolutions.jpg")
    model = load_model(f'model{test}')
    import timeit
    from gpiozero import CPUTemperature
    cpu = CPUTemperature()
    temps = [cpu.temperature]
    while 1:
        if CPUTemperature.temperature < 34:
            break
    start_time = timeit.default_timer()
    for i in range(iterations):
        run_model(model, image)
        temps.append(cpu.temperature)
    end_time = timeit.default_timer()
    result_time = end_time-start_time
    avg_time = result_time/iterations
    dtemp = temps[-1] - temps[0]
    import json
    data = {
        "cpu temperatures": temps,
        "delta temperature": dtemp,
        "average delta temperature": dtemp/iterations,
        "total time": result_time,
        "average time": avg_time
    }
    with open(f"test{test}.json", "w") as f:
        json.dump(data, f)

def load_image(path):
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image)
    image = tf.image.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    image_array = image.numpy()
    image_array = image_array.reshape(1, IMG_WIDTH, IMG_HEIGHT, 3)
    return image_array

def load_model(path):
    model = tf.saved_model.load(path)
    print(model.summary())
    return model

def run_model(model, data):
    return model(data)

if __name__ == "__main__":
    main()
