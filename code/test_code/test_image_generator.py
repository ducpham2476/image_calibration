import os
import math

import imutils
import numpy as np
from cv2 import cv2
import math

def image_generator(image_path, image_write_path):

    def image_zoom_out(image_data):
        region_of_interest = np.float32([[1, 0, 0], [0, 1, 0]])
        image_zoom = cv2.warpAffine(image_data, region_of_interest, (3000, 3000))
        image_shift = imutils.translate(image_zoom,
                                        (1500 - 1920/2),
                                        (1500 - 1080/2))
        return image_shift

    def image_output(image_write_path, image_data, filename, direction, y_value, x_value, rotate_value):
        image_path = "{}/{}_{}_({}_{}_{}).jpg".format(image_write_path,
                                                          filename,
                                                          direction,
                                                          y_value,
                                                          x_value,
                                                          rotate_value)
        cv2.imwrite(image_path, image_data)
        print(image_path)

        return

    def image_modifier(image_path, image_write_path, direction, generator_limit, generator_step):
        up_down = 90
        left_right = 0
        up_down_flag = 0
        left_right_flag = 0

        if direction == "up" or direction == "down":
            up_down_flag = 1
            if direction == "down":
                up_down = -90
        if direction == "left" or direction == "right":
            left_right_flag = 1
            if direction == "left":
                left_right = 180

        for filename in os.listdir(image_path):
            os.chdir(image_path)
            image_data = cv2.imread(filename)
            (image_height, image_width, r) = image_data.shape

            if direction == "rotation":
                for angle in range(-generator_limit, generator_limit, generator_step):
                    image_name = os.path.splitext(filename)[0]
                    rotation_matrix = cv2.getRotationMatrix2D((3000 // 2, 3000 // 2),
                                                              angle,
                                                              1.0
                                                              )
                    image_rotation = cv2.warpAffine(image_zoom_out(image_data),
                                                    rotation_matrix,
                                                    (3000, 3000)
                                                    )
                    image_cut = image_rotation[960:960 + image_height, 540:540 + image_width]

                    # print(image_write_path)
                    image_output(image_write_path=image_write_path,
                                 image_data=image_cut,
                                 filename=image_name,
                                 direction=direction,
                                 y_value=0,
                                 x_value=0,
                                 rotate_value=angle)

            else:
                image_data = image_zoom_out(image_data)

                for j in range(0, generator_limit + 1, generator_step):
                    image_name = os.path.splitext(filename)[0]
                    y_value = int(j * math.cos(left_right * math.pi / 180) * left_right_flag)
                    x_value = -int(j * math.sin(up_down * math.pi / 180) * up_down_flag)

                    image_shift = imutils.translate(image_data, y_value, x_value)
                    image_cut = image_shift[960:960 + image_height, 540:540 + image_width]
                    image_output(image_write_path=image_write_path,
                                 image_data=image_cut,
                                 filename=image_name,
                                 direction=direction,
                                 y_value=y_value,
                                 x_value=x_value,
                                 rotate_value=0)

        return



    print("Get user inputs")
    translation_limit   = int(input("Translation limit: "))
    rotation_limit      = int(input("Rotation limit: "))
    print("Generating images")

    image_modifier(image_path, image_write_path, "up", translation_limit, 10)
    print("*----")
    image_modifier(image_path, image_write_path, "down", translation_limit, 10)
    print("**---")
    image_modifier(image_path, image_write_path, "left", translation_limit, 10)
    print("***--")
    image_modifier(image_path, image_write_path, "right", translation_limit, 10)
    print("****-")
    image_modifier(image_path, image_write_path, "rotation", rotation_limit, 1)
    print("*****")

    print("Image generation finished!")

    return 0

source_path = "D:/generate_data/data_source"
generated_path = "D:/generate_data/data_generated"

image_generator(source_path, generated_path)