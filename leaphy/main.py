import image_operations, line_find, motor_operations, model_operations
import timeit, math

line_split = 5
if (line_split % 2) == 0:
    line_split += 1

model_image_compression = 10
line_interval = 0.1 #interval between line checks
model_interval = 0.5 #interval between model runs

def locate_line(img):
    #crop image
    line_img = image_operations.line_image(img, line_split)

    #find line pixels
    line_result = line_find.locate_line(line_img, line_split)
    return line_result

def run_model(img):
    #crop and resize image
    model_img = image_operations.model_image(img, model_image_compression)

    #execute model
    model_result = model_operations.execute_model(model_img)
    return model_result

def image():
    image_operations.picture()
    img = image_operations.load_image()
    return img

def main():
    middle_line = math.floor(line_split/2)
    last_line_time = timeit.timeit()
    last_model_time = timeit.timeit()
    current_speed = 1
    print()
    while True:
        img = image()
        if timeit.timeit() - last_line_time >= line_interval:
            print("Finding line")
            #check line
            line_result = locate_line(img)

            #react to line
            if line_result == middle_line:
                #line is in middle of frame
                print("Line is centred")
                motor_operations.leaphy.straight(current_speed)
            elif line_result < middle_line:
                #line is left of centre
                perc = 1/(line_result+1)
                print(f"Line is left, {perc} angle")
                motor_operations.leaphy.l_turn(perc, current_speed)
            elif line_result > middle_line:
                #line is right of centre
                perc = 1/(line_split-line_result)
                print(f"Line is right, {perc} angle")
                motor_operations.leaphy.r_turn(perc, current_speed)
            print()
        if timeit.timeit() - last_model_time >= model_interval:
            print("Running model")
            """
            Model:
            0 | Nothing
            1 | 50
            2 | 100
            """

            """
            model_result = run_model()
            if model_result == 1:
                current_speed = 0.5
            elif model_result == 2:
                current_speed = 1
            """

            print()

if __name__ == "__main__":
    main()