# Import required libraries
# System/OS functions
import os
# Image processing functions
import cv2
# Import folder/file manipulation functions
import folder_file_manipulation as ff_manip


# Define camera functions
def create_camera(username, password, ip, port, device_no):
	rtsp = "rtsp://" + username + ":" + password + "@" + ip + ":" + port + "/Streaming/channels/" + device_no

	return rtsp


def image_capture(rtsp):
	# Initiate video capture & take image frame
	capture = cv2.VideoCapture()
	capture.open(rtsp)

	# Additional information:
	# capture.set(10, 1920)
	# capture.set(10, 1080)
	# capture.set(10, 100)
	# Read the captured image
	read_status, image_data = capture.read()

	if not read_status:
		image_data = None

	return read_status, image_data


def image_save_path(path, input_name, image_type):
	# Define image save path:
	img_save_path = "{}/data_process/{}/{}".format(path, input_name, image_type)
	# Debug:
	# print(img_save_path)

	return img_save_path


# Capture image from camera, used for getting input of image_calibration main function
def auto_run_camera_capture(rtsp, parent, input_parking_lot):
	# Define save image path
	image_path = image_save_path(parent, input_parking_lot, "org")
	image_name = "{}_{}_{}.jpg".format("org", input_parking_lot, ff_manip.get_time_stamp())
	image_root = os.path.join(image_path, image_name)
	# Read image from camera RTSP link
	read_flag, image_data = image_capture(rtsp)
	# If image data is read in, write image and return image path, image data
	if read_flag:
		cv2.imwrite(image_root, image_data)

		return True, image_data, image_root, image_name
	# Else return null for return fields
	else:

		return False, None, "", ""


# Initiate camera default values
# These values should have a better way to get values
# rtsp_user = "admin"
# rtsp_password = "bk123456"
# ip_address = "192.168.0.115"
# access_port = "554"
# device_number = "1"
# Define image dimensions (width, height), in case of multiple input with different dimensions:
# image_dimension = (1920, 1080)
# Get current working directory
# parent_path = os.getcwd()

# def main_camera_function(path, input_name, image_type):
# 	# Get the rtsp hyperlink
# 	rtsp_hyperlink = create_camera(rtsp_user, rtsp_password, ip_address, access_port, device_number)
# 	# Get the image save path:
# 	current_save_path = image_save_path(path, input_name, image_type)
#
# 	# Get the image data from live camera
# 	read_flag, image_data = image_capture(rtsp_hyperlink)
#
# 	if read_flag:
# 		time_stamp = ff_manip.get_time_stamp()
# 		# Define image name & save path
# 		image_name = "{}_{}_{}.jpg".format(image_type, ff_manip.file_name_modify(input_name), time_stamp)
# 		image_path = os.path.join(current_save_path, image_name)
# 		# Write the image
# 		cv2.imwrite(image_path, image_data)
#
# 		return True, image_path
# 	else:
# 		print("Get image data failed!")
#
# 		return False, ""

# Test code
# Initiate values, for testing only

# parking_lot = "test_image"
# img_type = "std"
# runtime_variable = 0
# duration = 60
# # Execute main function!
# main_camera_function(parent_path, parking_lot, img_type)