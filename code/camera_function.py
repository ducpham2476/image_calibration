# Import required libraries
# System/OS functions
import os
# Image processing functions
import cv2
# Import folder/file manipulation functions
import folder_file_manipulation as ff_manip

# Initiate camera default values
# These values should have a better way to get values
rtsp_user = "admin"
rtsp_password = "bk123456"
ip_address = "192.168.30.115"
access_port = "554"
device_number = "1"
# Define image dimensions (width, height), in case of multiple input with different dimensions:
# image_dimension = (1920, 1080)
# Get current working directory
parent_path = os.getcwd()


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
	if read_status:
		# If image get an another input and does not match with the current designated resolution/dimensions
		# image = cv2.resize(image_data, image_dimension)
		image = image_data
		# Debug:
		# print("Image successfully captured")
	else:
		print("Read status: {}".format(read_status))
		print("Image not captured, please check the connection or the hardware")
		image = None

	return read_status, image


def image_save_path(path, input_name, image_type):
	# Define image save path:
	img_save_path = "{}\\data_process\\{}\\{}".format(path, input_name, image_type)
	# Debug:
	# print(img_save_path)

	return img_save_path


def main_camera_function(path, input_name, image_type):
	# Get the rtsp hyperlink
	rtsp_hyperlink = create_camera(rtsp_user, rtsp_password, ip_address, access_port, device_number)
	# Get the image save path:
	current_save_path = image_save_path(path, input_name, image_type)

	# Get the image data from live camera
	read_flag, image_data = image_capture(rtsp_hyperlink)
	# Debug:
	# cv2.imshow("Image", image_data)
	# cv2.waitKey(50)

	if read_flag:
		time_stamp = ff_manip.get_time_stamp()
		# Define image name & save path
		image_name = "{}_{}_{}.jpg".format(image_type, ff_manip.file_name_modify(input_name), time_stamp)
		image_path = os.path.join(current_save_path, image_name)
		# Write the image
		cv2.imwrite(image_path, image_data)
	else:
		print("Get image data failed!")

# Test code
# Initiate values, for testing only

# parking_lot = "test_image"
# img_type = "std"
# runtime_variable = 0
# duration = 60
# # Execute main function!
# main_camera_function(parent_path, parking_lot, img_type, runtime_variable, duration)

# Notes:
# Average capture time: around 1.5s/picture -> 40 pictures/minutes