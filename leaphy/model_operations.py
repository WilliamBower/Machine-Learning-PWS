import tensorflow as tf

model_path = "model.tflite"

def load_model():
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def execute_model(image):
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]
    prediction = predictions.index(max(predictions))
    return prediction

interpreter = load_model()