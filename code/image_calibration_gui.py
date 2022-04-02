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
# import threading
# import time
# import logging

# OpenCV package
import cv2

# Import additional functions
import folder_file_manipulation as folder_file_action
import landmark_recognition as landmark_action
import image_calibration
import image_additional_function as image_action
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Initiate working directories

# Define top working directory
parent = os.path.dirname(os.getcwd())                       # Top working directory
gui_dir = parent + "\\gui_files"                            # Graphical User Interface files
gui_code = parent + "\\code"                                # GUI functions' definitions
data_process_dir = parent + "\\data_process"

# Change current working directory to top directory
os.chdir(parent)
# Check and create storing data directory
folder_file_action.create_data_process(parent)
# Check and create text file contains list of parking lots
folder_file_action.create_parking_lot_manage("{}\\data_process".format(parent))
# Go to data top working directory
os.chdir("{}\\data_process".format(parent))
# Debug:
# print(os.getcwd())
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
previous_reference_filename = ""
select_parking_lot = ""
# Implement Undo/Redo action queue, used Define parking lot step
action_queue = deque()

# Create list of reference landmarks
number_of_landmarks = 4     # Number of parking lot reference landmarks, typically 4 for best transformations
number_of_slot = 0          # Number of parking lot slots, will be updated later in the program (if necessary)

# Global variables for bounding box's position currently on the screen
start_point_x = 0
start_point_y = 0
end_point_x = 0
end_point_y = 0

# Global variables for storing positions
ref_position_x = []         # Landmark, x position
ref_position_y = []         # Landmark, y position
slot_position_x = []        # Parking slot, x position
slot_position_y = []        # Parking slot, y position

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
    # Initiate Welcome Window on object creation
    def __init__(self):
        super(window_welcome, self).__init__()
        uic.loadUi(gui_dir + '\\open-window.ui', self)

        # quit = QtWidgets.QAction('Quit', self)
        # quit.triggered.connect(self.closeEvent)

        self.def_new_pl_B.clicked.connect(self.to_define_new)
        self.proc_auto_B.clicked.connect(self.to_run_auto)
        self.adj_pl_B.clicked.connect(self.to_adjust)
        self.exit_B.clicked.connect(self.exit_program)

    # Change to 2.1 > Define new parking lot Window
    @staticmethod
    def to_define_new():
        window.setCurrentWidget(window_define_new)

    # Change to 2.2 > Process Parking lot auto Window
    @staticmethod
    def to_run_auto():
        window.setCurrentWidget(window_run_auto)

    # Change to 2.3 > Adjust parking lots Window
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

        self.setWindowTitle("Exit?")
        self.setWindowIcon(QtGui.QIcon("{}\\icons\\exit_window_icon.png".format(gui_dir)))
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
        self.close()
        window.close()

    # Define reject on exit dialog
    def close_exit_prompt(self):
        # Close the dialog but not the main program
        self.reject()


# 2.1 > Define new parking lot menu:
class define_new_parkinglot(QMainWindow):
    # Initiate Welcome Window on object creation
    def __init__(self):
        super(define_new_parkinglot, self).__init__()
        uic.loadUi(gui_dir + '\\define-new-parking-lot.ui', self)

        self.next_B.clicked.connect(self.to_select_ref)
        self.back_B.clicked.connect(self.to_welcome)

        self.new_pl_name_textedit.cursorPositionChanged.connect(self.check_input_content)

        self.next_B.setEnabled(False)

    # Change to Select reference image Window
    # Get new parking lot name input from QLineEdit:new_pl_name_textedit, only if this name is valid & unused
    def to_select_ref(self):
        # Modify global variables
        global available_parking_lots, avail_lot_is_empty
        global select_parking_lot

        # Get new parking lot name, add to the available parking lot list, and create data storage directory
        # for the new parking lot
        parking_lot_name = self.new_pl_name_textedit.text()
        folder_file_action.file_append_avail_parking_lot(parent, parking_lot_name)
        folder_file_action.folder_manip(parent, parking_lot_name)
        folder_file_action.file_manip(parent, parking_lot_name)
        self.add_new_parking_lot(parking_lot_name)

        available_parking_lots, avail_lot_is_empty = folder_file_action.file_open_avail_parking_lot(parent)
        # Update the current parking lot list
        # available_parking_lots, avail_lot_is_empty = folder_file_action.file_open_avail_parking_lot(parent)
        # print(available_parking_lots)

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
        # Debug: Write input contents
        # print("Parking lot name:", parking_lot_name)

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
            # If the name is used: Return message & Block the next step
            # If the name is not used: Return message & Allow the next step
            for name in available_parking_lots:
                if parking_lot_name == name:
                    self.noti_box.setText("Parking lot already existed! Try an another name, or adjust the available "
                                          "parking lot instead!")
                    self.next_B.setEnabled(False)
                    return
                else:
                    self.noti_box.setText("Valid parking lot name!")
                    self.next_B.setEnabled(True)

    def add_new_parking_lot(self, write_name):
        temp_parking_lot = open("{}\\add_temporary_parking_lot.txt".format(data_process_dir), 'w+')
        temp_parking_lot.write(write_name)
        temp_parking_lot.close()

        # Clear previous input values
        self.noti_box.setText("Notifications")
        self.new_pl_name_textedit.clear()
        self.next_B.setEnabled(False)

        window_run_auto.add_parking_lot_list()
        window_adjust.refresh_parking_lot_list()


# 2.2 > Process parking lot auto menu:
class process_parkinglot_auto(QMainWindow):
    # Initiate Process Parking Lot Auto Window on object creation
    def __init__(self):
        super(process_parkinglot_auto, self).__init__()
        uic.loadUi(gui_dir + '\\process-parking-lot-auto.ui', self)

        for name in available_parking_lots:
            self.avail_parklot.addItem(name)

        self.run_auto_B.clicked.connect(self.process_data)
        self.run_auto_B.setEnabled(False)
        self.back_B.clicked.connect(self.to_welcome)
        self.def_new_sw_B.clicked.connect(self.to_define_new)

        self.avail_parklot.itemSelectionChanged.connect(self.adjust_selection)
        # self.show()

    def adjust_selection(self):
        if self.avail_parklot.currentItem() is None:
            self.run_auto_B.setEnabled(False)
        else:
            self.check_avail_ability()

    def check_avail_ability(self):
        global select_parking_lot

        parking_lot = self.avail_parklot.currentItem().text()
        if parking_lot == "":
            self.noti_box.setText("")
            self.run_auto_B.setEnabled(False)
        else:
            # print(parking_lot)
            data_path = "{}\\data_process\\{}".format(parent, parking_lot)
            if os.stat("{}\\defined_parking_lot.txt".format(data_path)).st_size != 0 and os.stat(
                    "{}\\landmarks.txt".format(data_path)).st_size != 0:
                self.noti_box.setText("Parking lot ready for calibration!")
                self.run_auto_B.setEnabled(True)

                select_parking_lot = parking_lot
            # print(data_path)
            else:
                self.run_auto_B.setEnabled(False)
                self.noti_box.setText("Parking lot is not defined. Please define parking lot before run!")

    def add_parking_lot_list(self):
        temp_parking_lots = open("{}\\add_temporary_parking_lot.txt".format(data_process_dir), "r+")
        new_parking_lots = temp_parking_lots.read()

        if os.stat("{}\\add_temporary_parking_lot.txt".format(data_process_dir)).st_size != 0:
            self.avail_parklot.addItem(new_parking_lots)
            # temp_parking_lots.truncate(0)
            temp_parking_lots.close()

    def delete_parking_lot(self, delete_name):
        if delete_name != "":
            delete_item = self.avail_parklot.findItems(delete_name, Qt.MatchContains)
            # print("Delete name: {}".format(delete_name))
            # print(delete_item)

            for item in delete_item:
                self.avail_parklot.takeItem(self.avail_parklot.row(item))

    @staticmethod
    def process_data():
        global ref_position_x, ref_position_y
        global reference_filename

        if select_parking_lot != "":
            run_flag = window_show_result.get_landmark_coordinates(select_parking_lot)
            if run_flag:
                window_show_result.image_calibration()
                reference_image_container = "{}\\{}\\defined_parking_lot.txt".format(data_process_dir,
                                                                                     select_parking_lot)
                f_reference_file = open(reference_image_container, 'r+')
                lines = f_reference_file.readlines()
                target_content = lines[0]
                reference_filename = target_content.replace("Reference Image: ", "").replace("\n", "")
                window_show_result.setup_original_image()
                window_show_result.setup_calibrated_image()

            window.setCurrentWidget(window_show_result)
            window_show_result.back_to_def_B.setEnabled(False)
            window_show_result.back_to_def_B.setStyleSheet("background-color: rgb(150, 150, 150)")

    @staticmethod
    def to_welcome():
        window.setCurrentWidget(window_starting)

    @staticmethod
    def to_define_new():
        window.setCurrentWidget(window_define_new)


# 2.3 > Adjust available parking lot
class adjust_parking_lot(QMainWindow):

    def __init__(self):
        super(adjust_parking_lot, self).__init__()
        uic.loadUi(gui_dir + '\\adjust-parking-lot.ui', self)

        for name in available_parking_lots:
            self.avail_pl_list.addItem(name)

        self.adjust_B.clicked.connect(self.to_image_browse)
        self.back_B.clicked.connect(self.to_welcome)
        self.delete_B.clicked.connect(self.delete_lot)

        self.avail_pl_list.itemSelectionChanged.connect(self.enable_disable_adjust)
        # if self.avail_pl_list.currentItem() == None:
        #     self.adjust_B.setEnabled(False)
        # else:
        #     self.adjust_B.setEnabled(True)
        self.enable_disable_adjust()
        self.refresh_parking_lot_list()

        # self.show()

    def to_image_browse(self):
        global select_parking_lot

        select_parking_lot = self.avail_pl_list.currentItem().text()

        window.setCurrentWidget(window_image_browser)

    def to_welcome(self):
        self.avail_pl_list.setCurrentItem(None)

        window.setCurrentWidget(window_starting)

    def enable_disable_adjust(self):
        if self.avail_pl_list.currentItem() is None:
            self.adjust_B.setEnabled(False)
            self.delete_B.setEnabled(False)
        else:
            self.adjust_B.setEnabled(True)
            self.delete_B.setEnabled(True)

    def delete_lot(self):
        global select_parking_lot

        delete_lot_name = self.avail_pl_list.currentItem().text()
        if delete_lot_name != "":
            folder_file_action.remove_all_contents("{}\\data_process\\{}".format(parent, delete_lot_name))
            folder_file_action.file_clear_specific_content(parent, "available_parking_lot.txt", delete_lot_name)
            list_item = self.avail_pl_list.selectedItems()
            if not list_item:
                return
            else:
                for item in list_item:
                    # print(item)
                    self.avail_pl_list.takeItem(self.avail_pl_list.row(item))
            # print("Deleted {} parking lot with all data".format(delete_lot_name))
            global available_parking_lots, avail_lot_is_empty
            available_parking_lots, avail_lot_is_empty = folder_file_action.file_open_avail_parking_lot(parent)

            select_parking_lot = ""

        self.refresh_parking_lot_list()
        window_run_auto.delete_parking_lot(delete_lot_name)

    def refresh_parking_lot_list(self):
        # refresh_list = threading.Timer(1.0, self.refresh_parking_lot_list)
        # threads.append(refresh_list)
        #
        # refresh_list.start()
        # Debug: Check working condition
        # Note: Should change print command to log, for debug purposes
        # print("Refresh list running")

        temp_parking_lots = open("{}\\add_temporary_parking_lot.txt".format(data_process_dir), "r+")
        new_parking_lots = temp_parking_lots.read()

        if os.stat("{}\\add_temporary_parking_lot.txt".format(data_process_dir)).st_size != 0:
            self.avail_pl_list.addItem(new_parking_lots)
            temp_parking_lots.truncate(0)
            temp_parking_lots.close()


# 3 > Select reference image
class image_browser(QMainWindow):
    global reference_filename

    def __init__(self):
        super(image_browser, self).__init__()                       # Call the inherited classes __init__ method
        uic.loadUi(gui_dir + '\\select-reference-image.ui', self)   # Load the .ui file

        self.next_B.clicked.connect(self.define_park_lot)
        self.browse_B.clicked.connect(self.browse_image)
        self.reset_image_B.clicked.connect(self.reset_image)
        self.cam_image_B.clicked.connect(self.camera_capture)

        self.back_B.clicked.connect(self.to_adjust)
        self.image_name.cursorPositionChanged.connect(self.check_reference_image)

        self.next_B.setEnabled(False)

    def to_adjust(self):
        self.reset_image()
        window.setCurrentWidget(window_adjust)

    def check_reference_image(self):
        if self.image_name.text() == "":
            self.next_B.setEnabled(False)
        else:
            self.next_B.setEnabled(True)

    @staticmethod
    def define_park_lot():
        # print(reference_filename)
        global reference_filename

        if reference_filename == "":

            return

        time_stamp = folder_file_action.get_time_stamp()
        reference_image = cv2.imread(reference_filename)
        write_path = "{}\\data_process\\{}\\std\\{}_std_{}.jpg".format(parent,
                                                                       select_parking_lot,
                                                                       select_parking_lot,
                                                                       time_stamp
                                                                       )
        cv2.imwrite(write_path, reference_image)

        parking_lot_defined = open("{}\\data_process\\{}\\defined_parking_lot.txt".format(parent,
                                                                                          select_parking_lot
                                                                                          ), "w+")
        parking_lot_defined.write("Reference Image: {}\n".format(write_path))
        parking_lot_defined.close()
        reference_filename = write_path

        window.setCurrentWidget(window_define_parking_lot)
        window_define_parking_lot.setup_image()

    def browse_image(self):
        global reference_filename

        # print("Browsing for reference image")
        filename = QFileDialog.getOpenFileName(self, 'Select File', parent, 'Images (*.png;*.jpg;*.jpeg)')
        self.image_name.setText(filename[0])
        # print(filename)
        # print(filename[0])
        reference_filename = filename[0]
        pixmap = QPixmap(filename[0])
        self.image_disp.setPixmap(pixmap)
        self.image_disp.setScaledContents(True)

        # print(reference_filename)

    def reset_image(self):
        global reference_filename

        # print("Reset image content")
        pixmap = QPixmap(None)
        self.image_name.setText("")
        reference_filename = ""
        self.image_disp.setPixmap(pixmap)

    def camera_capture(self):
        global reference_filename

        # print("Capture from Camera")
        # Import additional function to access the camera
        # Fix after retrieve the camera for an another test
        reference_filename = parent + '\\images\\camera-capture-dummy.jpg'
        pixmap = QPixmap(reference_filename)
        self.image_disp.setPixmap(pixmap)
        self.image_disp.setScaledContents(True)
        self.image_name.setText("Capture from Camera")


class define_parking_lot(QMainWindow):
    global reference_filename
    global previous_reference_filename

    def __init__(self):
        # Debug: Get image name
        # print(reference_filename)

        super(define_parking_lot, self).__init__()
        uic.loadUi(gui_dir + '\\define-parking-lot.ui', self)

        self.image_editor = image_painter(self.image_disp)
        self.image_editor.setGeometry(QtCore.QRect(0, 0, 960, 540))

        self.back_B.clicked.connect(self.select_reference_image)
        self.next_B.clicked.connect(self.to_result)
        self.next_B.setEnabled(False)

        self.undo_B.clicked.connect(self.undo_action)
        self.redo_B.clicked.connect(self.redo_action)
        self.reset_B.clicked.connect(self.reset_action)

        self.savelm_B.clicked.connect(self.get_landmark_index)
        self.saveplot_B.clicked.connect(self.get_parking_slot_index)

        self.setup_image()

    def setup_image(self):

        global reference_filename

        if reference_filename != "":
            input_image = cv2.imread(reference_filename)
            # cv2.imshow("Input image", input_image)
            # cv2.waitKey(1)
            resized_image = cv2.resize(input_image, (960, 540))
            # print(self.image_disp.width(), self.image_disp.height())
            # cv2.imshow("Resized image", resized_image)
            # cv2.waitKey(1)
            height, width, bytes_per_component = resized_image.shape
            # print(height, width)
            bytes_per_line = 3 * width
            # print(bytes_per_line)
            cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB, resized_image)
            # print("pass cvtColor")

            q_image = QtGui.QImage(resized_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
            # print("pass QImage")

            pixmap = QtGui.QPixmap.fromImage(q_image)
            # print("pass pixmap")
            self.image_editor.setPixmap(pixmap)
            # self.image_disp.setScaledContents(True)
            # print("pass set pixel map")

            self.image_editor = image_painter(self.image_disp)
            self.image_editor.setCursor(QtCore.Qt.CrossCursor)

            self.image_editor.update()

            # self.show()
            # reload_menu.cancel()
    def enable_next_step(self):
        if ref_position_x[1] != 0 and ref_position_x[2] != 0 and ref_position_x[3] != 0 and ref_position_x[4] != 0:
            self.next_B.setEnabled(True)
        else:
            self.next_B.setEnabled(False)

        return

    def get_landmark_index(self):
        global start_point_x, start_point_y, end_point_x, end_point_y
        global ref_position_x, ref_position_y

        index = int(input_dialog_prompt('landmark').get_data('landmark'))
        if index in range(1, 5):
            ref_position_x[index] = int((start_point_x + end_point_x)/2)
            # print(ref_position_x[index])
            ref_position_y[index] = int((start_point_y + end_point_y)/2)
            # print(ref_position_y[index])

            add_string = "Landmark {}: {}, {}".format(index, ref_position_x[index], ref_position_y[index])

            add_item = QListWidgetItem(add_string)
            self.listWidget.addItem(add_item)
            self.listWidget.setCurrentItem(add_item)

        self.enable_next_step()

        return

    def get_parking_slot_index(self):
        global number_of_slot
        global slot_position_x, slot_position_y

        if number_of_slot == 0:
            number_of_slot = int(input_dialog_prompt('number_of_parkslot').get_data('number_of_parkslot'))

            if number_of_slot > 0:
                for index in range(0, int(number_of_slot + 1)):
                    slot_position_x.append(0)
                    slot_position_y.append(0)
            else:
                # Break the input phase since the input is invalid
                return

        slot_index = int(input_dialog_prompt('parkslot').get_data('parkslot'))
        if slot_index in range(1, int(number_of_slot + 1)):
            slot_position_x[slot_index] = int((start_point_x + end_point_x) / 2)
            # print(ref_position_x[index])
            slot_position_y[slot_index] = int((start_point_y + end_point_y) / 2)
            # print(ref_position_y[index])

            add_string = "Slot {}: {}, {}".format(slot_index,
                                                  slot_position_x[slot_index],
                                                  slot_position_y[slot_index]
                                                  )
            add_item = QListWidgetItem(add_string)
            self.listWidget.addItem(add_item)
            self.listWidget.setCurrentItem(add_item)

    def text_manipulation(self):
        current_list_selection = self.listWidget.currentItem()

        if current_list_selection is None:
            # Return False, take no action later on
            return False, None
        else:
            current_string = self.listWidget.currentItem().text()
            # Return True & current item information
            temp_item = current_string.split(':')
            temp_string = "{}{}".format(temp_item[0], temp_item[1])

            selected_items = temp_string.split(' ')

            return True, selected_items

    def undo_action(self):
        global action_queue
        global ref_position_x, ref_position_y
        global slot_position_x, slot_position_y

        action_flag, values = self.text_manipulation()

        if action_flag is False:
            # Take no action, return to main program
            return
        else:
            if len(action_queue) > 50:
                # If the action queue has more than 50 entries, do nothing & return to the main program
                return
            action_queue.append(values)
            current_row = self.listWidget.currentRow()
            self.listWidget.takeItem(current_row)

            # Check which type of data was taken, delete the corresponding data from the program
            if values[0] == "Landmark":
                ref_position_x[int(values[1])] = 0
                ref_position_y[int(values[1])] = 0

            elif values[0] == "Slot":
                slot_position_x[int(values[1])] = 0
                slot_position_y[int(values[1])] = 0

            self.enable_next_step()

        return

    def redo_action(self):

        global action_queue
        global ref_position_x, ref_position_y
        global slot_position_x, slot_position_y

        if len(action_queue) == 0:

            return
        else:
            values = action_queue.pop()

            add_string = "{} {}: {} {}".format(values[0], values[1], values[2], values[3])
            add_item = QListWidgetItem(add_string)
            self.listWidget.addItem(add_item)
            self.listWidget.setCurrentItem(add_item)

            if values[0] == "Landmark":
                ref_position_x[int(values[1])] = int((values[2].split(","))[0])
                ref_position_y[int(values[1])] = int(values[3])

            elif values[0] == "Slot":
                slot_position_x[int(values[1])] = int((values[2].split(","))[0])
                slot_position_y[int(values[1])] = int(values[3])

        self.enable_next_step()

        return

    @staticmethod
    def reset_action():
        reset_prompt()

    @staticmethod
    def select_reference_image():
        window.setCurrentWidget(window_image_browser)

    @staticmethod
    def to_result():
        if (ref_position_x is not None) and (slot_position_x is not None):
            write_landmarks = open("{}\\data_process\\{}\\landmarks.txt".format(parent, select_parking_lot),
                                   'w+')
            for index in range(1, 5):
                write_landmarks.write("{} {}\n".format(ref_position_x[index], ref_position_y[index]))
            write_landmarks.close()

            write_parking_slot = open("{}\\data_process\\{}\\parking_slots.txt".format(parent, select_parking_lot),
                                      'w+')
            for index in range(1, int(number_of_slot + 1)):
                write_parking_slot.write("{} {} {}\n".format(index, slot_position_x[index], slot_position_y[index]))
            write_parking_slot.close()

        window_show_result.image_calibration()
        window_show_result.setup_original_image()
        window_show_result.setup_calibrated_image()

        window.setCurrentWidget(window_show_result)


class reset_prompt(QDialog):

    def __init__(self):
        super(reset_prompt, self).__init__()
        uic.loadUi('{}\\reset-prompt.ui'.format(gui_dir), self)

        self.setWindowTitle("Reset all data?")
        self.setWindowIcon(QtGui.QIcon("{}\\icons\\warning_icon.png".format(gui_dir)))
        self.yes_B.clicked.connect(self.reset_all_data)
        self.no_B.clicked.connect(self.close_reset_prompt)

        self.exec_()

    def reset_all_data(self):
        global ref_position_x, ref_position_y
        global slot_position_x, slot_position_y
        global number_of_slot
        global action_queue

        # Reset reference position, but do not delete their members since they need to be persist
        for index in range(1, 5):
            ref_position_x[index] = 0
            ref_position_y[index] = 0
        # Reset slot position list, delete all members since it needs to be redefine if reset
        slot_position_x.clear()
        slot_position_y.clear()
        number_of_slot = 0
        # Reset action queue as well
        action_queue.clear()

        # Remove all entries that exist on the list
        current_list_row = window_define_parking_lot.listWidget.currentRow()
        while current_list_row >= 0:
            window_define_parking_lot.listWidget.takeItem(current_list_row)
            current_list_row -= 1

        self.close()

        window_define_parking_lot.next_B.setEnabled(False)

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

        start_point_x = int(self.origin_x * 1920/960)
        start_point_y = int(self.origin_y * 1080/540)
        end_point_x = int(self.width * 1920/960)
        end_point_y = int(self.height * 1080/540)
        # Debug:
        # print(start_point_x, start_point_y, end_point_x, end_point_y)


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
        # self.accept()

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
        super(show_result, self).__init__()
        uic.loadUi(gui_dir + "\\results-show.ui", self)

        self.back_to_def_B.clicked.connect(self.to_define_parking_lot)

        self.com_ref_B.clicked.connect(self.compare_to_standard)
        self.acc_res_B.clicked.connect(self.close_program)

    def setup_original_image(self):
        # print(reference_filename)
        original_image = QPixmap(reference_filename)
        self.original_image_disp.setPixmap(original_image)
        self.original_image_disp.setScaledContents(True)

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

    @staticmethod
    def get_calibrated_images():

        list_calibrated = os.listdir("{}\\{}\\calib".format(data_process_dir, select_parking_lot))
        filename_calibrated = [name for name in list_calibrated
                               if os.path.isfile(os.path.join("{}\\{}\\calib".format(data_process_dir,
                                                                                     select_parking_lot),
                                                              name)
                                                 )
                               ]
        number_of_calibrated_file = len(filename_calibrated)
        del list_calibrated

        return number_of_calibrated_file, filename_calibrated

    def setup_calibrated_image(self):
        self.calib_image_label.setText("CALIBRATED IMAGE")

        number_of_calibrated_file, filename = self.get_calibrated_images()

        first_calib_image = "{}\\{}\\calib\\{}".format(data_process_dir,
                                                       select_parking_lot,
                                                       filename[0])

        calibrated_image_pixmap = QPixmap(first_calib_image)
        self.calib_image_disp.setPixmap(calibrated_image_pixmap)
        self.calib_image_disp.setScaledContents(True)
        self.com_ref_B.setText("COMPARE TO REFERENCE")
        self.com_ref_B.clicked.connect(self.compare_to_standard)

    def image_calibration(self):
        read_image = cv2.imread(parent+"\\images\\original_test.jpg")
        current_status, current_x, current_y = landmark_action.find_landmark(read_image)

        trigger_flag = \
            image_calibration.image_calibration(parent_path=parent,
                                                image_data=read_image,
                                                parklot_name=select_parking_lot,
                                                mode=0,
                                                filename="original_test.jpg",
                                                current_status=current_status,
                                                ref_x=ref_position_x,
                                                ref_y=ref_position_y,
                                                cur_x=current_x,
                                                cur_y=current_y)

        if trigger_flag:
            self.noti_box.setText("Image recovered successfully!")
        else:
            self.noti_box.setText("Image not recovered, please check debug.txt for more information!")

    @staticmethod
    def to_define_parking_lot():
        window.setCurrentWidget(window_define_parking_lot)

    @staticmethod
    def close_program():
        exit_dialog()

    def compare_to_standard(self):

        self.calib_image_label.setText("CALIBRATED IMAGE DIFFERENCE")
        number_of_calibrated_file, filename = self.get_calibrated_images()

        calib_image = "{}\\{}\\calib\\{}".format(data_process_dir,
                                                 select_parking_lot,
                                                 filename[0])
        temporary_path = "{}\\{}\\temp".format(data_process_dir,
                                               select_parking_lot)

        rate = image_action.image_difference(reference_filename, calib_image, temporary_path)

        difference_pixmap = QPixmap("{}\\temp_difference.jpg".format(temporary_path))
        self.calib_image_disp.setPixmap(difference_pixmap)
        self.calib_image_disp.setScaledContents(True)

        self.calib_rate_label.setText("RATING: {}%".format(rate))

        self.com_ref_B.setText("RETURN TO RESULT")
        self.com_ref_B.clicked.connect(self.setup_calibrated_image)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Main Program - Using PyQt5.uic to load the GUI
app = QApplication(sys.argv)

window = QtWidgets.QStackedWidget()

window_starting = window_welcome()
window_define_new = define_new_parkinglot()
window_run_auto = process_parkinglot_auto()
window_adjust = adjust_parking_lot()
window_image_browser = image_browser()
window_define_parking_lot = define_parking_lot()
window_show_result = show_result()

window.addWidget(window_starting)
window.addWidget(window_define_new)
window.addWidget(window_run_auto)
window.addWidget(window_adjust)
window.addWidget(window_image_browser)
window.addWidget(window_define_parking_lot)
window.addWidget(window_show_result)

window.setWindowTitle("Image Calibration")
window.setWindowIcon(QtGui.QIcon("{}\\icons\\main_program_icon.png".format(gui_dir)))
window.setCurrentWidget(window_starting)

window.setFixedWidth(1280)
window.setFixedHeight(720)
window.show()

app.exec_()