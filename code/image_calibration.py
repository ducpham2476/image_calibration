# Import required libraries
import os
import numpy as np
import cv2
import imutils
import datetime

import landmark_recognition
# Get top working directory

def image_calibration(parent_path, image_data, parklot_name, mode, filename, current_status, ref_x, ref_y, cur_x, cur_y):
	# Initiate values
	# Initiate values
	reference_x = []
	reference_y = []
	current_x = []
	current_y = []
	status = []

	for ii in range(0, 5):
		reference_x.append(ref_x[ii])
		reference_y.append(ref_y[ii])
		current_x.append(cur_x[ii])
		current_y.append(cur_y[ii])
		status.append(current_status[ii])

	def case_switch_mode():
		run_flag = 0  # Initiate run_flag, determine if the program could execute or not
		run_mode = 0  # Initiate run_mode, determine if the program run in 4 landmarks mode or 3 landmarks mode
		# run_mode = 1: 4 landmarks mode, run_mode = 0: 3 landmark mode
		cur_toggle = []  # List, determine which landmark could be used

		for i in range(0, 5):  # Initiate cur_toggle list, cur_toggle[0]:cur_toggle[5]
			cur_toggle.append(0)

		# sum_cur variable, quick check if the landmarks could be used or not
		sum_cur = status[1] + status[2] + status[3] + status[4]

		# Case: 4 landmarks found, usable!
		if sum_cur == 4:
			if status[1] == 1 and status[2] == 1 and status[3] == 1 and status[4] == 1:
				run_flag = 1
				run_mode = 1
			else:  # sum_cur is not correct, check the individuals
				if status[1] != 1:
					print("status[1] = ", status[1], ", <> 1, eliminate")
					cur_toggle[1] = 1
				if current_status[2] != 1:
					print("status[2] = ", status[2], ", <> 1, eliminate")
					cur_toggle[2] = 1
				if status[3] != 1:
					print("status[3] = ", status[3], ", <> 1, eliminate")
					cur_toggle[3] = 1
				if status[4] != 1:
					print("status[4] = ", status[4], ", <> 1, eliminate")
					cur_toggle[4] = 1
				print("Landmarks mismatch!")

		# Case: 3 landmarks found!
		elif sum_cur == 3:
			sum_toggle = 0  # sum_toggle variable, check if sum_cur actually returns 3 usable landmarks
			if status[1] != 1:
				cur_toggle[1] = 1
			if status[2] != 1:
				cur_toggle[2] = 1
			if status[3] != 1:
				cur_toggle[3] = 1
			if status[4] != 1:
				cur_toggle[4] = 1
			for i in range(0, 5):
				# Taking the sum of cur_toggle, if the value > 1 means there is more than 1 wrong landmark
				sum_toggle = sum_toggle + cur_toggle[i]
			if sum_toggle > 1:
				print("Landmark mismatch")
			else:
				# 3 valid landmarks, proceed to run!
				run_flag = 1
		else:
			print("Missing required landmarks!")

		return run_flag, run_mode, cur_toggle

	# Calculate the center (midpoint of ROI), used as a base for later transformation/rotation
	def midpoint_calculate(run_flag, run_mode, cur_toggle):	
		ref_midpoint_x = 0
		ref_midpoint_y = 0
		cur_midpoint_x = 0
		cur_midpoint_y = 0
		if run_flag == 1 and run_mode == 1:  # Calculate using all 4 landmarks
			for index in range(1, 5):
				ref_midpoint_x = ref_midpoint_x + reference_x[index]
				ref_midpoint_y = ref_midpoint_y + reference_y[index]
				cur_midpoint_x = cur_midpoint_x + current_x[index]
				cur_midpoint_y = cur_midpoint_y + current_y[index]
			ref_midpoint_x = int(ref_midpoint_x / 4)
			ref_midpoint_y = int(ref_midpoint_y / 4)
			cur_midpoint_x = int(cur_midpoint_x / 4)
			cur_midpoint_y = int(cur_midpoint_y / 4)
		elif run_flag == 1 and run_mode == 0:  # Calculate using 3 available landmarks only
			for index in range(1, 5):
				if cur_toggle[index] == 0:
					ref_midpoint_x = ref_midpoint_x + reference_x[index]
					ref_midpoint_y = ref_midpoint_y + reference_y[index]
					cur_midpoint_x = cur_midpoint_x + current_x[index]
					cur_midpoint_y = cur_midpoint_y + current_y[index]
			ref_midpoint_x = int(ref_midpoint_x / 3)
			ref_midpoint_y = int(ref_midpoint_y / 3)
			cur_midpoint_x = int(cur_midpoint_x / 3)
			cur_midpoint_y = int(cur_midpoint_y / 3)
		# Debug:
		# print("This function has been run")
		# print(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y)

		# else:   # run_flag
		# print("Landmark mismatch, program cannot execute!")

		return ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y

	# Calculate rotation angle using vector-based calculations
	def rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y, ref_xx, ref_yy, cur_xx, cur_yy):

		# Determine the reference vector & current vector
		ref_vector = [ref_xx - ref_midpoint_x, ref_yy - ref_midpoint_y]
		cur_vector = [cur_xx - cur_midpoint_x, cur_yy - cur_midpoint_y]

		unit_ref_vector = ref_vector / np.linalg.norm(ref_vector)
		unit_cur_vector = cur_vector / np.linalg.norm(cur_vector)
		dot_prod = np.dot(unit_ref_vector, unit_cur_vector)

		angle = np.arccos(dot_prod) * 180 / 3.1415

		# Debug:
		# print(angle)

		return angle

	def run_case(run_flag, run_mode, cur_toggle):
		# case variable for defining cases:
		# case = -1: Program error, not enough information for processing
		# case = 0: 4 landmarks mode
		# case = 1: 3 landmarks mode, landmark 01 eliminated from calculation due to error
		# case = 2: 3 landmarks mode, landmark 02 eliminated from calculation due to error
		# case = 3: 3 landmarks mode, landmark 03 eliminated from calculation due to error
		# case = 4: 3 landmarks mode, landmark 04 eliminated from calculation due to error
		case = -1  # Initiate case, default = -1 to prevent unwanted processing
		if run_flag == 1 and run_mode == 1:
			case = 0
		elif run_flag == 1 and run_mode == 0:
			if cur_toggle[1] == 1:
				case = 1
			if cur_toggle[2] == 1:
				case = 2
			if cur_toggle[3] == 1:
				case = 3
			if cur_toggle[4] == 1:
				case = 4
		else:  # Cannot process image, return error warning!
			case = -1
		# print("Not enough landmark information, please check the camera!")

		return case

	def zoom_image(img):
		# Initiate roi list/matrix, we only calculate on 2D plane
		roi = np.float32([[1, 0, 0], [0, 1, 0]])
		# Zoom out image
		# Expand the image to 3000 x 3000 px
		zoom = cv2.warpAffine(img, roi, (3000, 3000))
		# Matching the center point of the original image to the new center point of 3000 x 3000 px image
		shift_image = imutils.translate(zoom, (1500 - 1920 / 2), (1500 - 1080 / 2))
		# Debug: Show enlarged & shifted image
		# cv2.imshow("Test image", shift_image)
		# cv2.waitKey()

		return shift_image

	# Translation calibration main function
	def translation(shift_image, case, ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y):
		if case != -1:
			# Initiate values
			translation_x = ref_midpoint_x - cur_midpoint_x
			translation_y = ref_midpoint_y - cur_midpoint_y

			# If the shift is around 5 px, the translation is ignored
			# Landmark recognition might have small errors in calculating positions
			if translation_x in range(-3, 4):
				translation_x = 0
			if translation_y in range(-3, 4):
				translation_y = 0
			# Debug: Return value to check
			# print(trans_x, trans_y)

			# Return the original position
			shift_copy = shift_image
			shift_revert = imutils.translate(shift_copy, translation_x, translation_y)

		else:
			translation_x = 0
			translation_y = 0
			# Zoom out image
			shift = zoom_image(shift_image)
			# Do nothing, return the original image
			shift_revert = shift

		return shift_revert, translation_x, translation_y

	def rotation_case(cur_midpoint_x, cur_midpoint_y, cur_xx, cur_yy):

		standard_x_vector = [960, 0]
		standard_y_vector = [0, 540]
		rotate_vector = [cur_xx - cur_midpoint_x, cur_yy - cur_midpoint_y]
		unit_x_vector = standard_x_vector / np.linalg.norm(standard_x_vector)
		unit_y_vector = standard_y_vector / np.linalg.norm(standard_y_vector)
		unit_current_vector = rotate_vector / np.linalg.norm(rotate_vector)

		angle_with_x_axis = np.dot(unit_current_vector, unit_x_vector)
		angle_with_y_axis = np.dot(unit_current_vector, unit_y_vector)

		angle_sum = (angle_with_x_axis + angle_with_y_axis) * 180 / 3.1415

		if angle_sum > 90:
			return "counter clockwise"
		elif angle_sum < 90:
			return "clockwise"
		else:
			return "no rotation"

	def rotation(shift_image, case, ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y):

		# Initiate the values
		angle = []  # Rotation angle properties, angle[1]:angle[4] correspond to angle calculations
		# based on landmark01:landmark04
		angle_final = 0  # Average rotation angle
		for i in range(0, 5):  # Initiate angle list
			angle.append(0)

		# Debug:
		# print("Process case = ", case)
		# case = 0, 4 landmarks mode, calculation based on angle[1] and angle[4]
		if case == 0:
			angle[1] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
									reference_x[1], reference_y[1], current_x[1], current_y[1])
			angle[4] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
									reference_x[4], reference_y[4], current_x[4], current_y[4])
			angle_final = round((angle[1] + angle[4]) / 2)
			# If the current x[1] coordinate > reference x[1] coordinate, image has rotated clockwise, need to revert
			# with a negative angle
			if rotation_case(cur_midpoint_x, cur_midpoint_y, current_x[1], current_y[1]) == "counter clockwise":
				angle_final = -angle_final
		# Debug: Print angle[1], angle[4] & angle_final
		# print(angle[1], angle[4])
		# print(angle_final)
		# case = 2 or case = 3, 3 landmarks mode, calculation based on angle[1] and angle[4]
		if case == 2 or case == 3:
			angle[1] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
									reference_x[1], reference_y[1], current_x[1], current_y[1])
			angle[4] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
									reference_x[4], reference_y[4], current_x[4], current_y[4])
			angle_final = round((angle[1] + angle[4]) / 2)
			# If the current x[1] coordinate > reference x[1] coordinate, image has rotated clockwise, need to revert
			# with a negative angle
			if rotation_case(cur_midpoint_x, cur_midpoint_y, current_x[1], current_y[1]) == "clockwise":
				angle_final = -angle_final
		# Debug: Print angle[1], angle[4] & angle_final
		# print(angle[1], angle[4])
		# print(angle_final)
		if case == 1 or case == 4:
			angle[2] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
									reference_x[2], reference_y[2], current_x[2], current_y[2])
			angle[3] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
									reference_x[3], reference_y[3], current_x[3], current_y[3])
			angle_final = round((angle[2] + angle[3]) / 2)
			if rotation_case(cur_midpoint_x, cur_midpoint_y, current_x[2], current_y[2]) == "counter clockwise":
				angle_final = -angle_final
		# Debug: Print angle[2], angle[3] & angle_final
		# print(angle[2], angle[3])
		# print(angle_final)
		if case == -1:
			# Do nothing, return the original image. Print out a warning to the user
			print("Landmarks mismatched, image not processed, please check the camera/input")

			rotate_image = shift_image
			return rotate_image, 0
		# Debug:
		# print(angle_final)

		# Check if the angle is too large
		if angle_final in range(-15, 16):
			# Rotate the image
			shift_copy = shift_image
			# Debug:
			# cv2.imwrite(os.path.join("D:\\21_05_08_result\\debug", "debug.jpg"), shift_copy)
			rotate_mat = cv2.getRotationMatrix2D((3000 // 2, 3000 // 2), angle_final, 1.0)
			# Debug: Print debug value
			# cv2.imshow("Image", shift_copy)
			# cv2.waitKey()
			# print(rotate_mat)
			# Rotation calibration
			rotate_image = cv2.warpAffine(shift_copy, rotate_mat, (3000, 3000))
		else:
			print("Image is tilted too much, please check the camera")
			print("The image will not be rotated")

			rotate_image = shift_image

		return rotate_image, angle_final

	# Crop out the original image & save image function
	def save_image(path, img, case, translation_x, translation_y, angle):

		# Initiate height, width values. Avoid using constant, try using
		height = 1080
		width = 1920
		# Cut the desired image
		cut = img[960:960 + height, 540:540 + width]

		image_out = cut

		# Write down the desired image
		# Avoid using static addresses, try using environment variable instead!
		result_path = path + "\\data_process\\{}\\calib".format(parklot_name)              # Image save path
		name = os.path.splitext(filename)[0]                            # Separate filename, remove the extension
		cv2.imwrite(os.path.join(result_path, 'recov_{}_({}_{}_{}).jpg'.format(name, translation_x, translation_y,
																				angle)), image_out)
		# Log debug information
		f_debug = open(path + "\\data_process\\{}\\debug.txt".format(parklot_name), 'a+')
		f_debug.write("{}\n".format(datetime.datetime.now()))
		f_debug.write("filename: {}\n".format(name))
		f_debug.write("Working case: {}\n".format(case))

		if case != -1:
			print(filename, " recovered")
			f_debug.write(filename + " recovered\n")
		else:
			# cv2.imwrite(os.path.join(result_path, 'not_recov_{}.jpg'.format(name)), cut)
			print(filename, " not recovered, please check the camera/input")
			f_debug.write(filename + " not recovered, please check the camera/input\n")
		f_debug.write("\n")
		print("")

	run_fl, run_md, cur_togg = case_switch_mode()
	ref_mid_x, ref_mid_y, cur_mid_x, cur_mid_y = midpoint_calculate(run_fl, run_md, cur_togg)
	r_case = run_case(run_fl, run_md, cur_togg)

	# Debug:
	print("Working case:", r_case)
	# print(reference_x)
	# print(reference_y)
	# print(current_x)
	# print(current_y)
	# Zoom out image
	process_image = zoom_image(image_data)
	if mode == 0:
		# Perform image rotation calibration first
		rot_image, rot_angle = rotation(process_image, r_case, ref_mid_x, ref_mid_y, cur_mid_x, cur_mid_y)
		# Cut out the region of interest, update landmark values
		rot_image_cutout = rot_image[960:960 + 1080, 540:540 + 1920]
		status, current_x, current_y = landmark_recognition.find_landmark(rot_image_cutout)
		run_fl, run_md, cur_togg = case_switch_mode()
		ref_mid_x, ref_mid_y, cur_mid_x, cur_mid_y = midpoint_calculate(run_fl, run_md, cur_togg)
		r_case = run_case(run_fl, run_md, cur_togg)
		# With new landmark information, perform image translation calibration
		trans_image, trans_x, trans_y = translation(rot_image, r_case, ref_mid_x, ref_mid_y, cur_mid_x, cur_mid_y)
		# Save image as file
		save_image(parent_path, trans_image, r_case, trans_x, trans_y, rot_angle)

	# In case of running image translation calibration only:
	if mode == 2:
		trans_image, trans_x, trans_y = translation(process_image, r_case, ref_mid_x, ref_mid_y, cur_mid_x, cur_mid_y)
		rot_angle = 0
		save_image(parent_path, trans_image, r_case, trans_x, trans_y, rot_angle)
		
	# In case of running image rotation calibration only:
	elif mode == 1:
		trans_x = 0
		trans_y = 0
		rot_image, rot_angle = rotation(process_image, r_case, ref_mid_x, ref_mid_y, cur_mid_x, cur_mid_y)
		save_image(parent_path, rot_image, r_case, trans_x, trans_y, rot_angle)

	del status, current_x, current_y, reference_x, reference_y