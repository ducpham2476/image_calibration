import os
import io
import cv2
import ctypes

from PIL import Image, ImageTk


# Get native screen resolution, resize the image according to the ratio
def get_screen_resolution(ratio):
    user32 = ctypes.windll.user32
    screen_reso = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    screen_width = screen_reso[0]
    screen_height = screen_reso[1]
    width = int(screen_width * ratio)
    height = int(screen_height * ratio)

    return width, height


def get_img_data(f, max_size, first=False):
    img = Image.open(f)
    img.thumbnail(max_size, resample=Image.BICUBIC)
    if first:
        b_io = io.BytesIO()
        img.save(b_io, format="PNG")
        del img
        return b_io.getvalue()

    return ImageTk.PhotoImage(img)


def image_comparison(reference_image, calibrated_image, write_path):
    reference_data = cv2.imread(reference_image)
    calibrated_data = cv2.imread(calibrated_image)

    output = reference_data.copy()

    cv2.addWeighted(reference_data, 0.4, calibrated_data, 0.6, 0, output)
    cv2.imwrite(os.path.join(write_path, "temp.jpg"), output)


def image_difference(reference_image, calibrated_image, write_path):
    reference_data = cv2.imread(reference_image)
    calibrated_data = cv2.imread(calibrated_image)

    reference_grayscale = reference_data.copy()
    reference_grayscale = cv2.cvtColor(reference_grayscale, cv2.COLOR_BGR2GRAY)
    reference_grayscale = cv2.GaussianBlur(reference_grayscale, (5, 5), 0)

    calibrated_grayscale = calibrated_data.copy()
    calibrated_grayscale = cv2.cvtColor(calibrated_grayscale, cv2.COLOR_BGR2GRAY)
    calibrated_grayscale = cv2.GaussianBlur(calibrated_grayscale, (5, 5), 0)

    difference = cv2.absdiff(reference_grayscale, calibrated_grayscale)
    _, binary_difference = cv2.threshold(difference, 35, 255, cv2.THRESH_BINARY)

    pixel_matching_number = cv2.countNonZero(binary_difference)
    matching_rate = (1 - pixel_matching_number/(1920*1080)) * 100
    # print("Image matching rate = ", round(matching_rate, 4))

    cv2.imwrite(os.path.join(write_path, "temp_difference.jpg"), binary_difference)

    return round(matching_rate, 4)

"""
# Test code
original_image = "D:\\original_test.jpg"
standard_image = "D:\\standard_test.jpg"

matching_rate = image_difference(standard_image, original_image, "D:\\result")
"""