# Import required packages
# System package
import os
# Image processing - OpenCV package
import cv2
# import ctypes
# import io
# from PIL import Image, ImageTk


# Image comparison function, generate a mixed image between 2 input images
def image_comparison(reference_image, calibrated_image, write_path):
    # Read in 2 input images
    reference_data = cv2.imread(reference_image)
    calibrated_data = cv2.imread(calibrated_image)
    # Create the first layer of output image
    output = reference_data.copy()
    # Overlay the output with the 2nd image, using a weighted ratio
    cv2.addWeighted(reference_data, 0.4, calibrated_data, 0.6, 0, output)
    # Write the output image
    cv2.imwrite(os.path.join(write_path, "temp.jpg"), output)

    return


# Image difference function, calculates the difference of 2 input images by subtracting one image to the other one
def image_difference(reference_image, calibrated_image, write_path, start_roi_x, start_roi_y, end_roi_x, end_roi_y):
    # Read in reference image and calibrated image
    reference_data = cv2.imread(reference_image)
    calibrated_data = cv2.imread(calibrated_image)
    # Get grayscale image of reference image, apply Gaussian Blur to reduce noise
    reference_grayscale = reference_data.copy()
    reference_grayscale = cv2.cvtColor(reference_grayscale, cv2.COLOR_BGR2GRAY)
    reference_grayscale = cv2.GaussianBlur(reference_grayscale, (5, 5), 0)
    # Get grayscale image of calibrated image, apply Gaussian Blur to reduce noise
    calibrated_grayscale = calibrated_data.copy()
    calibrated_grayscale = cv2.cvtColor(calibrated_grayscale, cv2.COLOR_BGR2GRAY)
    calibrated_grayscale = cv2.GaussianBlur(calibrated_grayscale, (5, 5), 0)
    # Subtract reference image from calibrated image, get binary difference image (threshold = 35/255)
    difference = cv2.absdiff(reference_grayscale, calibrated_grayscale)
    _, binary_difference = cv2.threshold(difference, 35, 255, cv2.THRESH_BINARY)
    # Calculate the differences
    if start_roi_x == 0 and start_roi_y == 0 and end_roi_x == 0 and end_roi_y == 0:
        pixel_matching_number = cv2.countNonZero(binary_difference)
        matching_rate = (1 - pixel_matching_number / (1920*1080)) * 100
    elif (start_roi_x + start_roi_y + end_roi_x + end_roi_y) != 0:
        pixel_matching_number = cv2.countNonZero(binary_difference[start_roi_y:end_roi_y, start_roi_x:end_roi_x])
        matching_rate = (1 - pixel_matching_number/(abs(end_roi_x-start_roi_x)*abs(end_roi_y-start_roi_y))) * 100
    else:
        return -1
    # Write temporary binary difference image for display
    cv2.imwrite(os.path.join(write_path, "temp_difference.jpg"), binary_difference)

    return round(matching_rate, 3)

# Get native screen resolution, resize the image according to the ratio
# def get_screen_resolution(ratio):
#     user32 = ctypes.windll.user32
#     screen_reso = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#     screen_width = screen_reso[0]
#     screen_height = screen_reso[1]
#     width = int(screen_width * ratio)
#     height = int(screen_height * ratio)
#
#     return width, height

# def get_img_data(f, max_size, first=False):
#     img = Image.open(f)
#     img.thumbnail(max_size, resample=Image.BICUBIC)
#     if first:
#         b_io = io.BytesIO()
#         img.save(b_io, format="PNG")
#         del img
#         return b_io.getvalue()
#
#     return ImageTk.PhotoImage(img)

# ----------------------------------------------------------------------------------------------------------------------
# Function test
# original_image = "D:\\original_test.jpg"
# standard_image = "D:\\standard_test.jpg"
#
# matching_rate = image_difference(standard_image, original_image, "D:\\result")
# ----------------------------------------------------------------------------------------------------------------------