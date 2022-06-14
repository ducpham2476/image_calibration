# ----------------------------------------------------------------------------------------------------------------------
# Execute this file to run the main program

# For debug proposes, consider using logging functions instead of print() in future implementations
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Import required packages

# PyQt5 packages, for GUI building
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QApplication, QLabel, QMainWindow, QDialog, QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# System packages
import sys
import os
from collections import deque
import threading
# import time
# import logging

# OpenCV package
import cv2

# Import additional functions
# Import directory & file related functions
import folder_file_manipulation as folder_file_action
# Import landmarks processing functions
import landmark_recognition as landmark_action
# Import main image calibration function
import image_calibration
# Import additional computing functions
import image_additional_function as image_action
# Import camera functions
import camera_function

# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Initiate working directories

# Define top working directory
parent = os.path.dirname(os.getcwd())  # Top working directory
gui_dir = parent + "\\gui_files"  # Graphical User Interface files
gui_code = parent + "\\code"  # GUI functions' definitions
data_process_dir = parent + "\\data_process"

# Camera parameters:
rtsp_user = "admin"
rtsp_password = "bk123456"
ip_address = "192.168.30.115"
access_port = "554"
device_number = "01"
camera_rtsp = "rtsp://" + rtsp_user + ":" + rtsp_password + "@" + ip_address \
              + ":" + access_port + "/Streaming/channels/" + device_number

# Define the standard image is inputted through an online camera
std_camera_flag = False
# Define that the input data is from the online camera
calibrate_online_camera = False

# Change current working directory to top directory
os.chdir(parent)
# Check and create storing data directory
folder_file_action.create_data_process(parent)
# Check and create text file contains list of parking lots
folder_file_action.create_parking_lot_manage("{}\\data_process".format(parent))
# Go to data top working directory
os.chdir("{}\\data_process".format(parent))
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Initiate values

# Get list of available parking lots
available_parking_lots, avail_lot_is_empty = folder_file_action.file_open_avail_parking_lot(parent)
# Debug
# print(available_parking_lots)
# print("There is no parking lot:", avail_lot_is_empty)

# User defined parking lot image
reference_filename = ""
select_parking_lot = ""
current_calibrated_image = ""
# Implement Undo/Redo action queue, used Define parking lot step
action_queue = deque()

# Create list of reference landmarks
# Number of landmarks can be changed with different applications
number_of_landmarks = 4  # Number of reference landmarks, typically 4 for best transformations
number_of_slot = 0  # Number of parking lot slots, will be updated later in the program (if necessary)

# Global variables for image processing (temporary function)
image_index = -1
max_image_index = 0

# Global variables for bounding box's position currently on the screen
start_point_x = 0
start_point_y = 0
end_point_x = 0
end_point_y = 0

# Global variables for storing positions
ref_position_x = []  # Landmark, x position
ref_position_y = []  # Landmark, y position
slot_position_x = []  # Parking slot, x position
slot_position_y = []  # Parking slot, y position

# Global variables for Region of Interest (RoI)
start_roi_x = 0
start_roi_y = 0
end_roi_x = 0
end_roi_y = 0

# Initiate landmarks list
for i in range(0, number_of_landmarks + 1):
    ref_position_x.append(0)
    ref_position_y.append(0)


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Threads management
# threads = []
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Define .ui classes
# 1 > Welcome window:
class window_welcome(QMainWindow):
    # Initiate Welcome window on application execution
    def __init__(self):
        # Initiate object
        super(window_welcome, self).__init__()
        uic.loadUi(gui_dir + '\\open-window.ui', self)
        # Connect button to their functions
        self.def_new_pl_B.clicked.connect(self.to_define_new)
        self.proc_auto_B.clicked.connect(self.to_run_auto)
        self.adj_pl_B.clicked.connect(self.to_adjust)
        self.exit_B.clicked.connect(self.exit_program)

    # Change to 2.1 > Define New Parking Lot window
    @staticmethod
    def to_define_new():
        window.setCurrentWidget(window_define_new)

    # Change to 2.2 > Process Parking Lot Auto window
    @staticmethod
    def to_run_auto():
        window.setCurrentWidget(window_run_auto)

    # Change to 2.3 > Adjust Parking Lots window
    @staticmethod
    def to_adjust():
        window.setCurrentWidget(window_adjust)

    # Execute Exit dialog
    @staticmethod
    def exit_program():
        exit_dialog()


# 1 > Subclass: Exit Dialog
class exit_dialog(QDialog):
    # Initiate exit dialog on creation
    def __init__(self):
        super(exit_dialog, self).__init__()
        uic.loadUi('{}\\exit-prompt.ui'.format(gui_dir), self)
        # Set dialog title & icon
        self.setWindowTitle("Exit?")
        self.setWindowIcon(QtGui.QIcon("{}\\icons\\exit_window_icon.png".format(gui_dir)))
        # Connect buttons to their respective functions
        self.yes_B.clicked.connect(self.closeEvent)
        self.no_B.clicked.connect(self.close_exit_prompt)
        # Execute exit dialog
        self.exec_()

    # Overwrite closeEvent - Define behaviour on exit
    def closeEvent(self, event):
        # If a parking lot is selected and temporary folder contains files: Delete temp files
        if select_parking_lot != "":
            temporary_path = "{}\\{}\\temp".format(data_process_dir,
                                                   select_parking_lot)
            for filename in os.listdir(temporary_path):
                os.remove(os.path.join(temporary_path, filename))
        # Close the dialog and main program
        # Need to add threads management functions!
        # for threads in threading.enumerate():
        #     pass
        # Close dialog and main window
        self.close()
        window.close()

    # Define reject on exit dialog
    def close_exit_prompt(self):
        # Close the dialog but not the main program
        self.reject()


# 2.1 > Define new parking lot menu:
class define_new_parking_lot(QMainWindow):
    # Initiate Welcome Window on application execution
    def __init__(self):
        super(define_new_parking_lot, self).__init__()
        uic.loadUi(gui_dir + '\\define-new-parking-lot.ui', self)
        # Connect buttons to their respective functions
        self.next_B.clicked.connect(self.to_select_ref)
        self.back_B.clicked.connect(self.to_welcome)
        # Block next step as a default
        self.next_B.setEnabled(False)
        # Connect text edit box to input checking function
        self.new_pl_name_textedit.cursorPositionChanged.connect(self.check_input_content)

    # Change to Select reference image Window
    # Get new parking lot name input from QLineEdit:new_pl_name_textedit, only if this name is valid & unused
    def to_select_ref(self):
        # Modify global variables
        global available_parking_lots, avail_lot_is_empty
        global select_parking_lot
        # Get new parking lot name, create data storage directory, add to the available parking lot list
        # for the new parking lot
        parking_lot_name = self.new_pl_name_textedit.text()
        folder_file_action.file_append_avail_parking_lot(parent, parking_lot_name)
        folder_file_action.folder_manip(parent, parking_lot_name)
        folder_file_action.file_manip(parent, parking_lot_name)
        self.add_new_parking_lot(parking_lot_name)
        # Reload available parking lot list as the list is updated
        available_parking_lots, avail_lot_is_empty = folder_file_action.file_open_avail_parking_lot(parent)
        # Change to Select reference image
        window.setCurrentWidget(window_image_browser)
        # Set current parking lot to the new parking lot name
        select_parking_lot = parking_lot_name

    # Change back to Window Welcome
    @staticmethod
    def to_welcome():
        window.setCurrentWidget(window_starting)

    # Check user's input in the QLineEdit: new_pl_name_textedit. If the name is valid and unused, allow the user
    # to proceed to the next step
    def check_input_content(self):
        parking_lot_name = self.new_pl_name_textedit.text()
        # If there is no available parking lot: Accept the name & Let the user go to the next step
        if avail_lot_is_empty:
            self.noti_box.setText("Valid parking lot name!")
            self.next_B.setEnabled(True)
        # If the input box is empty: Return message & Block the next step
        if parking_lot_name == "":
            self.noti_box.setText("No parking lot name inserted! Try again")
            self.next_B.setEnabled(False)
        else:
            # If the input box is not empty and there are defined parking lots before: Check if the name is used or not
            # If the name is used: Return message & Block next step
            # If the name is not used: Return message & Allow next step
            for name in available_parking_lots:
                if parking_lot_name == name:
                    self.noti_box.setText("Parking lot already existed! Try an another name, or adjust the available "
                                          "parking lot instead!")
                    self.next_B.setEnabled(False)
                    # If the name is found on available list, break the loop to block this input
                    break
                else:
                    self.noti_box.setText("Valid parking lot name!")
                    self.next_B.setEnabled(True)

    # Add new parking lot to available parking lot list
    def add_new_parking_lot(self, write_name):
        # Write the parking lot name to a temporary file
        temp_parking_lot = open("{}\\add_temporary_parking_lot.txt".format(data_process_dir), 'w+')
        temp_parking_lot.write(write_name)
        temp_parking_lot.close()
        # Clear previous text edit box value
        self.noti_box.setText("Notifications")
        self.new_pl_name_textedit.clear()
        self.next_B.setEnabled(False)
        # Update on 2 parking lot selection list (from Window 2.2 and Window 2.3)
        window_run_auto.add_parking_lot_list()
        window_adjust.refresh_parking_lot_list()


# 2.2 > Process parking lot auto menu:
class process_parking_lot_auto(QMainWindow):
    # Initiate Process Parking Lot Auto Window on application execution
    def __init__(self):
        super(process_parking_lot_auto, self).__init__()
        uic.loadUi(gui_dir + '\\process-parking-lot-auto.ui', self)
        # Load available parking lot into selection list
        for name in available_parking_lots:
            self.avail_parklot.addItem(name)
        # Connect buttons to their functions
        self.run_auto_B.clicked.connect(self.process_data)
        self.run_auto_B.setEnabled(False)
        self.back_B.clicked.connect(self.to_welcome)
        self.def_new_sw_B.clicked.connect(self.to_define_new)
        # Connect parking lot list selection to a check function
        # check if a parking lot is selected and has it been defined or not
        self.avail_parklot.itemSelectionChanged.connect(self.adjust_selection)

    # Block the access to next step if no parking lot is selected
    def adjust_selection(self):
        # If no parking lot is selected, block the next step
        if self.avail_parklot.currentItem() is None:
            self.run_auto_B.setEnabled(False)
        else:
            # If a parking lot is selected, check if the parking lot is defined or not
            self.check_avail_ability()

    # Check the definition of the selected parking lot
    def check_avail_ability(self):
        global select_parking_lot
        # Get current parking lot name (extract from the selection on the list)
        parking_lot = self.avail_parklot.currentItem().text()
        # If the name is None, block the next step
        if parking_lot == "":
            self.noti_box.setText("")
            self.run_auto_B.setEnabled(False)
        # Else check the selected parking lot's data
        else:
            # Access to the respective data storage of the parking lot
            data_path = "{}\\data_process\\{}".format(parent, parking_lot)
            # Check the availability of reference image and landmarks information
            if os.stat("{}\\defined_parking_lot.txt".format(data_path)).st_size != 0 and \
                    os.stat("{}\\landmarks.txt".format(data_path)).st_size != 0:
                # If both info available, allow access to the next step
                self.noti_box.setText("Parking lot ready for calibration!")
                self.run_auto_B.setEnabled(True)
                # Set current parking lot
                select_parking_lot = parking_lot
            # If the requirements do not meet, block the next step
            else:
                self.run_auto_B.setEnabled(False)
                self.noti_box.setText("Parking lot is not defined. Please define parking lot before run!")

    # Add new parking lot if there is(are) ones added through Define New Parking Lot
    def add_parking_lot_list(self):
        # Read new parking lot name from a temporary file
        temp_parking_lots = open("{}\\add_temporary_parking_lot.txt".format(data_process_dir), "r+")
        new_parking_lots = temp_parking_lots.read()
        # If there are data within the temporary file, append them to the available parking lot list
        if os.stat("{}\\add_temporary_parking_lot.txt".format(data_process_dir)).st_size != 0:
            self.avail_parklot.addItem(new_parking_lots)
            # temp_parking_lots.truncate(0)
            temp_parking_lots.close()

    # Delete parking lot if there is(are) one(s) deleted through Adjust Parking Lot
    def delete_parking_lot(self, delete_name):
        # If a parking lot(s) is indicated, find it(them) on the available parking lot list
        if delete_name != "":
            # Add deleted one(s) into a temporary list
            delete_item = self.avail_parklot.findItems(delete_name, Qt.MatchContains)
            for item in delete_item:
                # Remove those from the available parking lot list
                self.avail_parklot.takeItem(self.avail_parklot.row(item))

    # Execute process parking lot auto function
    # Static method means this function does not take the "self" as an argument
    @staticmethod
    def process_data():
        global ref_position_x, ref_position_y
        global start_roi_x, start_roi_y, end_roi_x, end_roi_y
        global reference_filename

        # Read data from Region of Interest file
        region_of_interest_path = "{}\\data_process\\{}\\roi.txt".format(parent, select_parking_lot)
        # Check if the region of interest exists and has data
        if os.path.isfile("{}\\data_process\\{}\\roi.txt".format(parent, select_parking_lot)) and \
                os.stat("{}\\data_process\\{}\\roi.txt".format(parent, select_parking_lot)).st_size != 0:
            f_roi = open(region_of_interest_path, 'r+')
            value_string = f_roi.readlines()[0]
            values = value_string.split(" ")
            # Assign global values to determine region of interest within the image
            start_roi_x = int(values[0])
            start_roi_y = int(values[1])
            end_roi_x = int(values[2])
            end_roi_y = int(values[3])

        # If a parking lot is selected
        if select_parking_lot != "":
            # Get landmarks information from defined data of the parking lot
            run_flag = window_show_result.get_landmark_coordinates(select_parking_lot)
            # If the data is valid, run image calibration
            if run_flag:
                # Get reference image information
                reference_image_container = "{}\\{}\\defined_parking_lot.txt".format(data_process_dir,
                                                                                     select_parking_lot)
                f_reference_file = open(reference_image_container, 'r+')
                lines = f_reference_file.readlines()
                target_content = lines[0]
                reference_filename = target_content.replace("Reference Image: ", "").replace("\n", "")
                # Set up standard image at the Show Result window
                window_show_result.setup_standard_image()
                # Run image calibration
                window_show_result.image_calibration()
                # window_show_result.setup_calibrated_image()
            # Move to Show Result window
            window.setCurrentWidget(window_show_result)
            # Disable Back to Define mode button, as the program is running automatically
            window_show_result.back_to_def_B.setEnabled(False)
            window_show_result.back_to_def_B.setStyleSheet("background-color: rgb(150, 150, 150)")

    # Move back to Welcome window
    @staticmethod
    def to_welcome():
        window.setCurrentWidget(window_starting)

    # Move to Define New Parking Lot window
    @staticmethod
    def to_define_new():
        window.setCurrentWidget(window_define_new)


# 2.3 > Adjust available parking lot
class adjust_parking_lot(QMainWindow):
    # Initiate Adjust Parking Lot window on application execution
    def __init__(self):
        super(adjust_parking_lot, self).__init__()
        uic.loadUi(gui_dir + '\\adjust-parking-lot.ui', self)
        # Append all available parking lot to list widget
        for name in available_parking_lots:
            self.avail_pl_list.addItem(name)
        # Connect buttons to their functions
        self.adjust_B.clicked.connect(self.to_image_browse)
        self.back_B.clicked.connect(self.to_welcome)
        self.delete_B.clicked.connect(self.delete_lot)
        # Connect list widget selection to flow control function
        # If no parking lot is selected, the program will block access to the next step
        self.avail_pl_list.itemSelectionChanged.connect(self.enable_disable_adjust)
        # Update flow control 
        self.enable_disable_adjust()
        # self.refresh_parking_lot_list()

    # Move to Image browser window, using current selected parking lot
    def to_image_browse(self):
        global select_parking_lot
        # Get parking lot name from list selection
        select_parking_lot = self.avail_pl_list.currentItem().text()
        # Move to Image Browser window
        window.setCurrentWidget(window_image_browser)

    # Move back to Welcome window
    def to_welcome(self):
        # Clear current option
        self.avail_pl_list.setCurrentItem(None)
        # Move to Welcome window
        window.setCurrentWidget(window_starting)

    # Check if any parking lot is selected. If not, block the next step
    def enable_disable_adjust(self):
        # If current selected item is blank/None, block the next step
        if self.avail_pl_list.currentItem() is None:
            self.adjust_B.setEnabled(False)
            self.delete_B.setEnabled(False)
        # Else allow access
        else:
            self.adjust_B.setEnabled(True)
            self.delete_B.setEnabled(True)

    @staticmethod
    # Delete selected parking lot from the list, as well as its data
    def delete_lot():
        delete_prompt()

    # Add new parking lot to the list widget
    def refresh_parking_lot_list(self):
        # Get temporary new parking lots
        temp_parking_lots = open("{}\\add_temporary_parking_lot.txt".format(data_process_dir), "r+")
        new_parking_lots = temp_parking_lots.read()
        # If the temporary parking lot file is not empty, add all entity from the file
        if os.stat("{}\\add_temporary_parking_lot.txt".format(data_process_dir)).st_size != 0:
            self.avail_pl_list.addItem(new_parking_lots)
            # Truncate the file (clear contents after adding)
            # This line should be deprecated!
            temp_parking_lots.truncate(0)
            temp_parking_lots.close()


# 2> Subclass: Delete Dialog: Used to get user confirmation upon Parking lot data deletion
class delete_prompt(QDialog):
    global select_parking_lot

    def __init__(self):
        super(delete_prompt, self).__init__()
        uic.loadUi('{}\\delete-prompt.ui'.format(gui_dir), self)

        self.setWindowTitle("Delete {}?".format(select_parking_lot))
        self.setWindowIcon(QtGui.QIcon("{}\\icons\\warning_icon.png".format(gui_dir)))
        self.yes_B.clicked.connect(self.delete_parking_lot)
        self.no_B.clicked.connect(self.close_delete_prompt)

        self.exec_()

    def delete_parking_lot(self):
        global select_parking_lot
        global available_parking_lots, avail_lot_is_empty

        # Get parking lot name to delete
        delete_lot_name = window_adjust.avail_pl_list.currentItem().text()
        # If the parking lot name is not blank/empty string
        if delete_lot_name != "":
            # Remove all data belongs to the parking lot (directory tree & files)
            folder_file_action.remove_all_contents("{}\\data_process\\{}".format(parent, delete_lot_name))
            # Remove the parking lot from saved parking lot list
            folder_file_action.file_clear_specific_content(parent, "available_parking_lot.txt", delete_lot_name)
            # Remove from the selection list
            list_item = window_adjust.avail_pl_list.selectedItems()
            if list_item is not None:
                for item in list_item:
                    window_adjust.avail_pl_list.takeItem(window_adjust.avail_pl_list.row(item))
            # Update the current available parking lot list
            available_parking_lots, avail_lot_is_empty = folder_file_action.file_open_avail_parking_lot(parent)
            # Update parking lot list/Check if this line is necessary
            # self.refresh_parking_lot_list()
            # Delete the corresponding parking lot from Process Parking Lot Auto menu
            window_run_auto.delete_parking_lot(delete_lot_name)
            # Clear current parking lot name
            select_parking_lot = ""
            # Close the prompt
            self.close()

    def close_delete_prompt(self):
        self.reject()


# 3 > Select reference image window
class image_browser(QMainWindow):
    global reference_filename

    # Initiate Image Browser window on application execution
    def __init__(self):
        super(image_browser, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi(gui_dir + '\\select-reference-image.ui', self)  # Load the .ui file
        # Connect buttons to their functions
        self.next_B.clicked.connect(self.define_park_lot)
        self.browse_B.clicked.connect(self.browse_image)
        self.reset_image_B.clicked.connect(self.reset_image)
        self.cam_image_B.clicked.connect(self.camera_capture)
        self.back_B.clicked.connect(self.to_adjust)
        # Connect reference image path box to flow control function
        # If the reference image path is empty, or invalid, block the next step
        self.image_name.cursorPositionChanged.connect(self.check_reference_image)
        # Disable next button as default
        self.next_B.setEnabled(False)

    # Move back to Adjust Parking Lot window
    def to_adjust(self):
        self.reset_image()
        window.setCurrentWidget(window_adjust)

    # Check the availability of the reference image
    def check_reference_image(self):
        # If the image path is empty, block the next step
        if self.image_name.text() == "":
            self.next_B.setEnabled(False)
        else:
            image_path = self.image_name.text()
            # If the image path leads to a valid file
            if os.path.isfile(image_path):
                self.next_B.setEnabled(True)
            # Else block the next step
            else:
                self.next_B.setEnabled(False)

    # Move to Define Parking Lot window
    @staticmethod
    def define_park_lot():
        global reference_filename
        global std_camera_flag

        # If the reference image file path is blank/empty string, do nothing
        if reference_filename == "":
            return
        # Else save the reference image to the standard image directory of the current parking lot
        if std_camera_flag is False:
            # Get time stamp of the definition
            time_stamp = folder_file_action.get_time_stamp()
            # Read and write the image at the selection time
            reference_image = cv2.imread(reference_filename)
            write_path = "{}\\data_process\\{}\\std\\std_{}_{}.jpg".format(parent,
                                                                           select_parking_lot,
                                                                           select_parking_lot,
                                                                           time_stamp
                                                                           )
            cv2.imwrite(write_path, reference_image)
            # Write the reference image path to a storage file
            parking_lot_defined = open("{}\\data_process\\{}\\defined_parking_lot.txt".format(parent,
                                                                                              select_parking_lot
                                                                                              ), "w+")
            parking_lot_defined.write("Reference Image: {}\n".format(write_path))
            parking_lot_defined.close()
            # Set reference image path
            reference_filename = write_path
        # Set up the reference image file for definition on the window
        window_define_parking_lot.setup_image()
        # Move to Define Parking Lot window
        window.setCurrentWidget(window_define_parking_lot)

    # Browse for reference image
    def browse_image(self):
        global reference_filename
        # Restrict available files to image file only
        filename = QFileDialog.getOpenFileName(self, 'Select File', parent, 'Images (*.png;*.jpg;*.jpeg)')
        # Get image path, set to the image name box
        self.image_name.setText(filename[0])
        # Set reference file path to selected image
        reference_filename = filename[0]
        # Set up image preview box
        pixmap = QPixmap(filename[0])
        self.image_disp.setPixmap(pixmap)
        self.image_disp.setScaledContents(True)

    # Reset selected reference image
    def reset_image(self):
        global reference_filename
        # Reset preview image box to blank
        pixmap = QPixmap(None)
        self.image_disp.setPixmap(pixmap)
        # Clear image path/image source indicator from the input box
        self.image_name.setText("")
        reference_filename = ""

    # Capture standard image using camera
    def camera_capture(self):
        # Access to global reference image file, and selected parking lot
        global reference_filename, select_parking_lot
        # Check camera flag
        global std_camera_flag
        # Get standard image write folder
        current_write_folder = "{}\\data_process\\{}\\{}".format(parent, select_parking_lot, "std")
        # Capture from camera
        read_status, image_data = camera_function.image_capture(camera_rtsp)
        # Write standard image
        time_stamp = folder_file_action.get_time_stamp()
        image_name = "{}_{}_{}.jpg".format("std", select_parking_lot, time_stamp)
        reference_filename = os.path.join(current_write_folder, image_name)
        cv2.imwrite(reference_filename, image_data)
        # Check image availability, then setup reference image
        if read_status and os.path.isfile(reference_filename):
            # If image is read in (and successfully saved), read in the image captured from camera
            # QPixmap requires passing in image path, not image data
            pixmap = QPixmap(reference_filename)
            self.image_disp.setPixmap(pixmap)
            self.image_disp.setScaledContents(True)
            self.image_name.setText("Capture from Camera")
            # Write standard image path to save file
            parking_lot_defined = open("{}\\data_process\\{}\\defined_parking_lot.txt".format(parent,
                                                                                              select_parking_lot
                                                                                              ), "w+")
            parking_lot_defined.write("Reference Image: {}\n".format(reference_filename))
            parking_lot_defined.close()
            std_camera_flag = True
            # Enable next step
            self.next_B.setEnabled(True)

            return
        # Else clear reference image path, set to no image has been captured
        else:
            # Clear current standard image
            reference_filename = ""

            return


# 4 > Define Parking Lot window
class define_parking_lot(QMainWindow):

    # Initiate Define Parking Lot window on application execution
    def __init__(self):
        super(define_parking_lot, self).__init__()
        uic.loadUi(gui_dir + '\\define-parking-lot.ui', self)
        # Set image viewer box, overload with custom QLabel class
        self.image_editor = image_painter(self.image_disp)
        self.image_editor.setGeometry(QtCore.QRect(0, 0, 960, 540))
        # Connect buttons to their respective functions
        self.back_B.clicked.connect(self.select_reference_image)
        # Connect navigation buttons
        self.undo_B.clicked.connect(self.undo_action)
        self.redo_B.clicked.connect(self.redo_action)
        self.reset_B.clicked.connect(self.reset_action)
        # Connect save type buttons
        self.savelm_B.clicked.connect(self.get_landmark_index)
        self.saveplot_B.clicked.connect(self.get_parking_slot_index)
        self.save_roi_B.clicked.connect(self.get_region_of_interest)
        # Connect to the execute function, and disable it as a default
        self.next_B.clicked.connect(self.to_result)
        self.next_B.setEnabled(False)

    # Setup selected standard image to the image preview box
    def setup_image(self):
        # Access to the global standard image path
        global reference_filename
        # If reference image is a valid image
        if os.path.isfile(reference_filename):
            # Setup reference image for Parking lot definition
            input_image = cv2.imread(reference_filename)
            resized_image = cv2.resize(input_image, (960, 540))
            height, width, bytes_per_component = resized_image.shape
            bytes_per_line = 3 * width
            cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB, resized_image)
            # Set pixel map as the selected image
            q_image = QtGui.QImage(resized_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(q_image)
            # Overlay the image on to the designated QLabel
            self.image_editor.setPixmap(pixmap)
            self.image_editor.setCursor(QtCore.Qt.CrossCursor)

    # Check if the parking lot is defined or not. Enable next step only if the parking lot has enough information
    # for executing
    def enable_next_step(self):
        # Access to global reference point positions
        global ref_position_x, ref_position_y
        # Check if all landmarks are defined. If yes, enable next step
        if ref_position_x[1] != 0 and ref_position_x[2] != 0 and ref_position_x[3] != 0 and ref_position_x[4] != 0:
            self.next_B.setEnabled(True)
        # Else, disable the next step as default
        else:
            self.next_B.setEnabled(False)

    # Save landmark coordinates via image painter
    def get_landmark_index(self):
        # Access to global variables: Bounding box start and end points, reference point coordinates,
        # standard image path
        global start_point_x, start_point_y, end_point_x, end_point_y
        global ref_position_x, ref_position_y
        global reference_filename

        # Get landmark index value
        index = int(input_dialog_prompt('landmark').get_data('landmark'))
        # If the landmark index is within the acceptable range (from 1 to 4), enable auto landmark detection to increase
        # the accuracy
        if index in range(1, 5):
            # Find the biggest yellow landmark within the small image defined by the boundaries
            # Get the small image cut out from the large standard image
            small_image = \
                landmark_action.image_get_data(reference_filename,
                                               start_point_x,
                                               start_point_y,
                                               end_point_x,
                                               end_point_y)
            # Calculate the x-coordinate and y-coordinate offset of the landmark centroid from the small image
            x_offset, y_offset = landmark_action.landmark_definition(small_image)
            # Calculate the position of the landmark accordingly to the standard image
            ref_position_x[index] = start_point_x + x_offset
            ref_position_y[index] = start_point_y + y_offset
            # Write the information onto GUI
            add_string = "Landmark {}: {}, {}".format(index, ref_position_x[index], ref_position_y[index])
            add_item = QListWidgetItem(add_string)
            self.listWidget.addItem(add_item)
            self.listWidget.setCurrentItem(add_item)
        # Run the checker to enable the next step
        self.enable_next_step()

    # Save parking slot coordinates via image painter
    def get_parking_slot_index(self):
        # Access to global variables: Bounding box start and end points, parking slot start and end coordinates,
        # number of available parking slot on the field
        global start_point_x, start_point_y, end_point_x, end_point_y
        global number_of_slot
        global slot_position_x, slot_position_y
        # If the parking lot has no parking slot (value == 0), enable prompt to get the number of parking slots first
        if number_of_slot == 0:
            number_of_slot = int(input_dialog_prompt('number_of_parkslot').get_data('number_of_parkslot'))
            # If number of slot is a valid natural number, append to the current slot position lists an amount
            # of participants equals to the number of slot
            if number_of_slot > 0:
                for index in range(0, int(number_of_slot + 1)):
                    slot_position_x.append(0)
                    slot_position_y.append(0)
            # Else break the input phase since the input is invalid
            else:

                return
        # Get parking lot slot index value
        slot_index = int(input_dialog_prompt('parkslot').get_data('parkslot'))
        # If the index is in the valid range (defined value above), get the slot centroid as slot position
        if slot_index in range(1, int(number_of_slot + 1)):
            slot_position_x[slot_index] = int((start_point_x + end_point_x) / 2)
            slot_position_y[slot_index] = int((start_point_y + end_point_y) / 2)
            # Write the saved information to the GUI
            add_string = "Slot {}: {}, {}".format(slot_index,
                                                  slot_position_x[slot_index],
                                                  slot_position_y[slot_index]
                                                  )
            add_item = QListWidgetItem(add_string)
            self.listWidget.addItem(add_item)
            self.listWidget.setCurrentItem(add_item)

    # Save Region of Interest on the image via image painter
    def get_region_of_interest(self):
        # Access to global variables: Bounding box start and end points, region of interest coordinates
        global start_point_x, start_point_y, end_point_x, end_point_y
        global start_roi_x, start_roi_y
        global end_roi_x, end_roi_y

        # Save the values
        start_roi_x = start_point_x
        start_roi_y = start_point_y
        end_roi_x = end_point_x
        end_roi_y = end_point_y

        # Write saved values to the GUI
        add_string = "RoI: {} {}, {} {}".format(start_roi_x, start_roi_y, end_roi_x, end_roi_y)
        add_item = QListWidgetItem(add_string)
        self.listWidget.addItem(add_item)
        self.listWidget.setCurrentItem(add_item)

        # Write ROI information to save file
        f_roi = open("{}\\data_process\\{}\\roi.txt".format(parent, select_parking_lot), 'w+')
        f_roi.write("{} {} {} {}".format(start_roi_x, start_roi_y, end_roi_x, end_roi_y))
        f_roi.close()

        return

    # Manipulate text values that appear on the parking lot definition list. Used in Undo/Redo actions.
    # Applies to landmark coordinates, parking slot coordinates, region of interest
    def text_manipulation(self):
        # Get current list selection
        current_list_selection = self.listWidget.currentItem()
        # If no item of the list is selected, return False & take no action later on
        if current_list_selection is None:

            return False, None
        # Else grab the text value of the selection, return True & current item information
        else:
            current_string = self.listWidget.currentItem().text()
            # Remove colon ':' symbol
            temp_item = current_string.split(':')
            temp_string = "{}{}".format(temp_item[0], temp_item[1])
            # Remove hyphen ',' symbol
            temp_item = temp_string.split(',')
            temp_string = "{}{}".format(temp_item[0], temp_item[1])
            # Split string using white space, return list of values
            selected_items = temp_string.split(' ')

            return True, selected_items

    # Undo previous parking lot defining action
    def undo_action(self):
        # Access to global values:
        # - action_queue: A list of performed actions: Save landmark/Save parking slot/Save Region of Interest
        # - ref_position_x, ref_position_y: Reference landmark positions
        # - slot_position_x, slot_position_y: Parking slot positions
        # - *_roi_*: Region of interest position
        global action_queue
        global ref_position_x, ref_position_y
        global slot_position_x, slot_position_y
        global start_roi_x, start_roi_y, end_roi_x, end_roi_y
        # Get the action flag (check if there was any action performed), together with its values
        action_flag, values = self.text_manipulation()
        # If there was at least one action
        if action_flag:
            # If the undo button is executed more than 50 times, do nothing & return to the main program
            if len(action_queue) > 50:

                return
            # Add extracted values to the action queue, serves as the basic material for building back the action
            action_queue.append(values)
            # Remove the action's entry on the list appears on the menu
            current_row = self.listWidget.currentRow()
            self.listWidget.takeItem(current_row)
            # Check which type of data was taken, delete the corresponding data from the program
            # Landmark:
            if values[0] == "Landmark":
                ref_position_x[int(values[1])] = 0
                ref_position_y[int(values[1])] = 0
            # Parking slot:
            elif values[0] == "Slot":
                slot_position_x[int(values[1])] = 0
                slot_position_y[int(values[1])] = 0
            # Region of interest:
            elif values[0] == "RoI":
                start_roi_x = start_roi_y = end_roi_x = end_roi_y = 0
            # Check if the landmarks condition still meets? All four of the landmarks need to be defined!
            self.enable_next_step()

        return

    # Redo previous parking lot defining action
    def redo_action(self):
        # Access to global values:
        # - action_queue: A list of performed actions: Save landmark/Save parking slot/Save Region of Interest
        # - ref_position_x, ref_position_y: Reference landmark positions
        # - slot_position_x, slot_position_y: Parking slot positions
        # - *_roi_*: Region of interest position
        global action_queue
        global ref_position_x, ref_position_y
        global slot_position_x, slot_position_y
        global start_roi_x, start_roi_y, end_roi_x, end_roi_y

        # If action_queue has at least an action stored within, put that action back to the parking lot definition
        if len(action_queue) != 0:
            # Remove the action from the action_queue
            values = action_queue.pop()
            # If the action was defining the Region of interest, the string format is different from the rest
            if values[0] == "RoI":
                # Adding the values back to their respective container
                start_roi_x = values[1]
                start_roi_y = values[2]
                end_roi_x   = values[3]
                end_roi_y   = values[4]
                # Define the string to add back to the list
                add_string = "RoI: {} {}, {} {}".format(values[1], values[2], values[3], values[4])
            else:
                # Adding the values back to their respective container
                if values[0] == "Landmark":
                    ref_position_x[int(values[1])] = int(values[2])
                    ref_position_y[int(values[1])] = int(values[3])

                elif values[0] == "Slot":
                    slot_position_x[int(values[1])] = int(values[2])
                    slot_position_y[int(values[1])] = int(values[3])
                # Define the string to add back to the list
                add_string = "{} {}: {}, {}".format(values[0], values[1], values[2], values[3])
            # Append the action back to the action list on the menu
            add_item = QListWidgetItem(add_string)
            self.listWidget.addItem(add_item)
            self.listWidget.setCurrentItem(add_item)
        # Check if the landmarks condition still meets? All four of the landmarks need to be defined!
        self.enable_next_step()

        return

    # Reset/Delete all parking lot defining action(s)
    @staticmethod
    def reset_action():
        # Run the reset prompt
        reset_prompt()

    # Return to Select reference image Window
    @staticmethod
    def select_reference_image():
        window.setCurrentWidget(window_image_browser)

    # Execute Image Calibration main function, then move to the Show result Window
    @staticmethod
    def to_result():
        # If there are new data about the landmark positions, write to the save file
        if ref_position_x is not None:
            write_landmarks = open("{}\\data_process\\{}\\landmarks.txt".format(parent, select_parking_lot), 'w+')
            for index in range(1, 5):
                write_landmarks.write("{} {}\n".format(ref_position_x[index], ref_position_y[index]))
            write_landmarks.close()

        # If there are new data about the parking slot positions, write to the save file
        if slot_position_x is not None:
            write_parking_slot = open("{}\\data_process\\{}\\parking_slots.txt".format(parent, select_parking_lot),
                                      'w+')
            for index in range(1, int(number_of_slot + 1)):
                write_parking_slot.write("{} {} {}\n".format(index, slot_position_x[index], slot_position_y[index]))
            write_parking_slot.close()

        # Run image calibration once, then move to the Show result Window
        window_show_result.image_calibration()
        window_show_result.setup_standard_image()
        window.setCurrentWidget(window_show_result)


# Reset/Delete all parking lot define action - prompt, a derived class of QDialog
class reset_prompt(QDialog):
    # Reset prompt initiation upon object creation
    def __init__(self):
        super(reset_prompt, self).__init__()
        uic.loadUi('{}\\reset-prompt.ui'.format(gui_dir), self)
        # Set prompt name & icon
        self.setWindowTitle("Reset all data?")
        self.setWindowIcon(QtGui.QIcon("{}\\icons\\warning_icon.png".format(gui_dir)))
        # Connect buttons to their respective functions
        self.yes_B.clicked.connect(self.reset_all_data)
        self.no_B.clicked.connect(self.close_reset_prompt)
        # Execute the prompt
        self.exec_()

    # If yes, reset all data
    def reset_all_data(self):
        # Access to global variables:
        # - ref_position_*: Landmark positions
        # - slot_position_* : Parking slot positions
        # - *_roi_*: Image region of interest positions
        # - number_of_slot: Number of parking slot that can be defined
        # - action_queue: List of parking lot defining actions that has been appended through Undo action
        global ref_position_x, ref_position_y
        global slot_position_x, slot_position_y
        global start_roi_x, start_roi_y, end_roi_x, end_roi_y
        global number_of_slot
        global action_queue
        # Reset reference position, but do not delete their members
        for index in range(1, 5):
            ref_position_x[index] = 0
            ref_position_y[index] = 0
        # Reset slot position list, delete all members
        slot_position_x.clear()
        slot_position_y.clear()
        number_of_slot = 0
        # Reset Region of Interest
        start_roi_x = start_roi_y = end_roi_x = end_roi_y = 0
        # Reset action queue as well
        action_queue.clear()
        # Remove all entries that exist on the list
        current_list_row = window_define_parking_lot.listWidget.currentRow()
        while current_list_row >= 0:
            window_define_parking_lot.listWidget.takeItem(current_list_row)
            current_list_row -= 1
        # Close the prompt as the function completes
        self.close()
        # Block the next step as the landmarks now are not defined
        window_define_parking_lot.next_B.setEnabled(False)

    # If no, close the prompt without execute the delete function
    def close_reset_prompt(self):
        self.reject()


class image_painter(QLabel):
    origin_x = 0
    origin_y = 0
    width = 0
    height = 0
    flag = False

    def mousePressEvent(self, event):
        self.flag = True
        self.origin_x = event.x()
        self.origin_y = event.y()

    def mouseReleaseEvent(self, event):
        self.flag = False

    def mouseMoveEvent(self, event):
        if self.flag:
            self.width = event.x()
            self.height = event.y()
            self.update()

    def paintEvent(self, event):
        global start_point_x, start_point_y, end_point_x, end_point_y

        super().paintEvent(event)
        if (self.width - self.origin_x <= 5) and (self.height - self.origin_y <= 5):
            rectangle = QtCore.QRect(0, 0, 0, 0)
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine))
            painter.drawRect(rectangle)
        else:
            rectangle = QtCore.QRect(self.origin_x, self.origin_y,
                                     self.width - self.origin_x,
                                     self.height - self.origin_y)
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine))
            painter.drawRect(rectangle)

        start_point_x   = round(self.origin_x   * 1920 / 960)
        start_point_y   = round(self.origin_y   * 1080 / 540)
        end_point_x     = round(self.width      * 1920 / 960)
        end_point_y     = round(self.height     * 1080 / 540)


class input_dialog_prompt(QDialog):

    def __init__(self, dialog_type):
        super(input_dialog_prompt, self).__init__()
        uic.loadUi(gui_dir + '\\get-index-prompt.ui', self)

        self.setWindowIcon(QtGui.QIcon("{}\\icons\\info_icon.png".format(gui_dir)))

        if dialog_type == 'landmark':
            self.input_name_label.setText("Enter landmark index")
            self.setWindowTitle("Landmark index")
        elif dialog_type == 'parkslot':
            self.input_name_label.setText("Enter parking slot index")
            self.setWindowTitle("Parking slot index")
        elif dialog_type == 'number_of_parkslot':
            self.input_name_label.setText("Enter number of parking slot")
            self.setWindowTitle("Number of parking slot")

        self.input_B.clicked.connect(self.check_value_input)

    def check_value_input(self):
        input_value = self.input_lineedit.text()

        if input_value.strip().isdigit():
            self.accept()

            return input_value

    @staticmethod
    def get_data(dialog_type):
        # Initiate index input dialog
        dialog = input_dialog_prompt(dialog_type)
        # Execute input dialog
        dialog.exec_()

        return dialog.check_value_input()


class show_result(QMainWindow):
    def __init__(self):
        global image_index, max_image_index

        super(show_result, self).__init__()
        uic.loadUi(gui_dir + "\\results-show.ui", self)

        self.back_to_def_B.clicked.connect(self.to_define_parking_lot)

        self.com_ref_B.clicked.connect(self.compare_to_standard)
        self.acc_res_B.clicked.connect(self.close_program)

    def setup_standard_image(self):
        standard_image = QPixmap(reference_filename)
        self.standard_image_disp.setPixmap(standard_image)
        self.standard_image_disp.setScaledContents(True)

    # For Process Parking Lot Automatically method
    @staticmethod
    def get_landmark_coordinates(select_lot):
        global ref_position_x, ref_position_y

        landmark_file_destination = "{}\\{}\\landmarks.txt".format(data_process_dir, select_lot)
        f_landmark = open(landmark_file_destination, 'r+')

        if os.stat(landmark_file_destination).st_size == 0:

            return False
        else:
            lis = [line.split() for line in f_landmark]
            coordinates = []
            n = len(lis[0])
            file_length = len(lis)

            for jndex in range(n):
                temp_array = []
                for index in range(file_length):
                    temp_array.append(int(lis[index][jndex]))
                coordinates.append(temp_array)

            ref_position_x[1] = coordinates[0][0]
            ref_position_y[1] = coordinates[1][0]
            ref_position_x[2] = coordinates[0][1]
            ref_position_y[2] = coordinates[1][1]
            ref_position_x[3] = coordinates[0][2]
            ref_position_y[3] = coordinates[1][2]
            ref_position_x[4] = coordinates[0][3]
            ref_position_y[4] = coordinates[1][3]

            return True

    # Get newly captured image
    def setup_captured_image(self, image_name):

        image_path = "{}\\data_process\\{}\\{}\\{}".format(parent, select_parking_lot, "org", image_name)
        capture_image = QPixmap(image_path)
        self.original_image_disp.setPixmap(capture_image)
        self.original_image_disp.setScaledContents(True)

    @staticmethod
    def get_calibrated_images():
        global calibrate_online_camera
        global data_process_dir, select_parking_lot

        if not calibrate_online_camera:
            list_calibrated = os.listdir("{}\\{}\\calib".format(data_process_dir, select_parking_lot))
            filename_calibrated = [name for name in list_calibrated
                                   if os.path.isfile(os.path.join("{}\\{}\\calib".format(data_process_dir,
                                                                                         select_parking_lot),
                                                                  name)
                                                     )
                                   ]
            number_of_calibrate_file = len(filename_calibrated)

            return number_of_calibrate_file, filename_calibrated
        else:

            return 0, ""

    def setup_calibrated_image(self):
        # global image_index
        global current_calibrated_image

        self.calib_image_label.setText("CALIBRATED IMAGE")

        # Deprecated calibrated image selection
        # number_of_calibrated_file, filename = self.get_calibrated_images()
        #
        # last_calib_image = "{}\\{}\\calib\\{}".format(data_process_dir,
        #                                               select_parking_lot,
        #                                               filename[image_index])

        calibrated_image_pixmap = QPixmap(current_calibrated_image)
        self.calib_image_disp.setPixmap(calibrated_image_pixmap)
        self.calib_image_disp.setScaledContents(True)

        self.com_ref_B.setText("COMPARE TO REFERENCE")
        self.com_ref_B.clicked.connect(self.compare_to_standard)

    def image_calibration(self):
        global image_index, max_image_index
        global current_calibrated_image
        global calibrate_online_camera

        if calibrate_online_camera is False:
            # Read in image and get filename
            image_data, image_name = self.image_read()
            if image_data is None or image_name is None:
                # Insert a control function here
                # print("Program finished!")
                return
            else:
                current_status, current_x, current_y = landmark_action.find_landmark(image_data, ref_position_x, ref_position_y)

                trigger_flag, current_calibrated_image = \
                    image_calibration.image_calibration(parent_path=parent,
                                                        image_data=image_data,
                                                        parklot_name=select_parking_lot,
                                                        mode=0,
                                                        filename=image_name,
                                                        current_status=current_status,
                                                        ref_x=ref_position_x,
                                                        ref_y=ref_position_y,
                                                        cur_x=current_x,
                                                        cur_y=current_y)
                if trigger_flag:
                    self.noti_box.setText("Image recovered successfully!")
                else:
                    self.noti_box.setText("Image not recovered, please check debug.txt for more information!")
                # Show result
                self.setup_captured_image(image_name)
                self.setup_calibrated_image()
                self.calculate_rating()

                # Start autorun procedure
                if image_index <= max_image_index - 1:
                    run_timer = threading.Timer(5, self.auto_run)
                    run_timer.start()

                    return

        elif calibrate_online_camera is True:
            read_flag, image_data, image_root, image_name = camera_function.auto_run_camera_capture(camera_rtsp,
                                                                                                    parent,
                                                                                                    select_parking_lot)
            if read_flag is True:
                if image_data is None:
                    return
                else:
                    current_status, current_x, current_y = landmark_action.find_landmark(image_data, ref_position_x, ref_position_y)
                    trigger_flag, current_calibrated_image = \
                        image_calibration.image_calibration(parent_path=parent,
                                                            image_data=image_data,
                                                            parklot_name=select_parking_lot,
                                                            mode=0,
                                                            filename=image_name,
                                                            current_status=current_status,
                                                            ref_x=ref_position_x,
                                                            ref_y=ref_position_y,
                                                            cur_x=current_x,
                                                            cur_y=current_y)
                    if trigger_flag is True:
                        self.noti_box.setText("Image recovered successfully!")
                    else:
                        self.noti_box.setText("Image not recovered, please check debug.txt for more information!")

                    self.setup_captured_image(image_name)
                    self.setup_calibrated_image()
                    self.calculate_rating()

                    run_timer = threading.Timer(2, self.auto_run)
                    run_timer.start()

                    return

    @staticmethod
    def image_parse():
        original_image_path = "{}\\data_process\\{}\\org".format(parent, select_parking_lot)
        file_list_original = os.listdir(original_image_path)
        file_name_original = [filename for filename in file_list_original if os.path.isfile(
            os.path.join(original_image_path, filename))]
        number_of_file = len(file_name_original)

        return number_of_file, file_name_original

    def image_selection(self):
        global image_index, max_image_index

        original_image_path = "{}\\data_process\\{}\\org".format(parent, select_parking_lot)
        number_of_file, file_name_list = self.image_parse()
        max_image_index = number_of_file - 1
        image_index = image_index + 1
        if image_index > max_image_index:
            return "Finished"
        else:
            return os.path.join(original_image_path, file_name_list[image_index]), file_name_list[image_index]

    def image_read(self):
        image_path, image_name = self.image_selection()

        if os.path.isfile(image_path):
            image_data = cv2.imread(image_path)
            return image_data, image_name
        else:
            return None, None

    @staticmethod
    def to_define_parking_lot():
        window.setCurrentWidget(window_define_parking_lot)

    def calculate_rating(self):
        global image_index, reference_filename
        global start_roi_x, start_roi_y, end_roi_x, end_roi_y
        global current_calibrated_image

        self.com_ref_B.setEnabled(False)
        # number_of_calibrated_file, filename = self.get_calibrated_images()
        #
        # calib_image = "{}\\{}\\calib\\{}".format(data_process_dir,
        #                                          select_parking_lot,
        #                                          filename[image_index])

        temporary_path = "{}\\{}\\temp".format(data_process_dir,
                                               select_parking_lot)

        rate = image_action.image_difference(reference_filename,
                                             current_calibrated_image,
                                             temporary_path,
                                             start_roi_x,
                                             start_roi_y,
                                             end_roi_x,
                                             end_roi_y)

        self.calib_rate_label.setText("RATING: {}%".format(rate))
        self.com_ref_B.setEnabled(True)

        return

    def compare_to_standard(self):
        global image_index

        self.calib_image_label.setText("DIFFERENCE")

        temporary_path = "{}\\{}\\temp".format(data_process_dir,
                                               select_parking_lot)

        difference_pixmap = QPixmap("{}\\temp_difference.jpg".format(temporary_path))
        self.calib_image_disp.setPixmap(difference_pixmap)
        self.calib_image_disp.setScaledContents(True)

        self.com_ref_B.setText("RETURN TO RESULT")
        self.com_ref_B.clicked.connect(self.setup_calibrated_image)

    def auto_run(self):
        global image_index, max_image_index
        global calibrate_online_camera
        global start_roi_x, start_roi_y, end_roi_x, end_roi_y

        print("Region of interest: ({}, {}), ({}, {})".format(start_roi_x, start_roi_y, end_roi_x, end_roi_y))
        self.image_calibration()

        # print(image_index, max_image_index)
        # print(threading.enumerate())

    @staticmethod
    def close_program():
        exit_dialog()


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Additional functions
def camera_parameters_modifier(new_username, new_password, new_ip, new_port, new_device_number):
    global rtsp_user, rtsp_password
    global ip_address, access_port, device_number

    def username_modifier(new_value):
        global rtsp_user
        if new_value is not None and len(new_value) > 0:
            rtsp_user = new_value
            return True
        else:
            return False

    def password_modifier(new_value):
        global rtsp_password
        if new_value is not None and len(new_value) > 0:
            rtsp_password = new_value
            return True
        else:
            return False

    def ip_modifier(new_value):
        global ip_address
        if new_value is not None and len(new_value) > 0:
            ip_address = new_value
            return True
        else:
            return False

    def port_modifier(new_value):
        global access_port
        if int(new_value) in range(0, 10000):
            access_port = new_value
            return True
        else:
            return False

    def device_number_modifier(new_value):
        global device_number
        if new_value is not None and len(new_value) > 0:
            device_number = new_value
            return True
        else:
            return False

    modify_user = username_modifier(new_username)
    modify_pass = password_modifier(new_password)
    modify_ip = ip_modifier(new_ip)
    modify_port = port_modifier(new_port)
    modify_dev_no = device_number_modifier(new_device_number)

    return modify_user, modify_pass, modify_ip, modify_port, modify_dev_no


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Main Program - Using PyQt5.uic to load the GUI
app = QApplication(sys.argv)

window = QtWidgets.QStackedWidget()

window_starting = window_welcome()
window_define_new = define_new_parking_lot()
window_run_auto = process_parking_lot_auto()
window_adjust = adjust_parking_lot()
window_image_browser = image_browser()
window_define_parking_lot = define_parking_lot()
window_show_result = show_result()

window.addWidget(window_starting)
window.addWidget(window_define_new)
window.addWidget(window_run_auto)
window.addWidget(window_adjust)
window.addWidget(window_image_browser)
window.addWidget(window_show_result)

window.setWindowTitle("Image Calibration")
window.addWidget(window_define_parking_lot)
window.setWindowIcon(QtGui.QIcon("{}\\icons\\main_program_icon.png".format(gui_dir)))
window.setCurrentWidget(window_starting)

window.setFixedWidth(1280)
window.setFixedHeight(720)
window.show()

app.exec_()