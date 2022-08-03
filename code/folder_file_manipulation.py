# Import required libraries
import os.path
from os import path

from datetime import datetime as dt


# Create data top working directory
def create_data_process(parent_path):
    if not path.exists(parent_path + "/data_process"):
        os.mkdir("data_process")
        # print("Data directory created!")


# Create required working directory if needed
def folder_manip(parent_path, input_name):
    # Debug: Data parent working directory
    # print(parent_path)
    # Debug: Create ./data_process directory for test, in case the directory is yet to exist
    # if not path.exists(parent_path + "/data_process"):
    #     os.mkdir("data_process")

    # Move to data top directory
    os.chdir(parent_path + "/data_process")

    # Debug: Print the parent folder name
    # print(path_parent)

    # Define folder_make command:
    def folder_make(folder_name):
        if not path.exists(folder_name):
            os.mkdir(folder_name)
            # print(folder_name + ' created!')
        else:
            pass
            # print(folder_name + ' existed!')
        return

    # Create folder with name
    folder_make(input_name)
    os.chdir("./{}".format(input_name))
    # Create sub-directories
    folder_make("std")
    folder_make("org")
    folder_make("calib")
    # folder_make("log_files")
    folder_make("temp")

    # Return the folder pointer to main folder
    os.chdir(parent_path)
    folder_make("debug")
    # Debug: Print current working directory
    # print(os.getcwd())

    # print(os.listdir)


def create_parking_lot_manage(parent_path):
    if not path.isfile(parent_path + "/available_parking_lot.txt"):
        f = open("{}/available_parking_lot.txt".format(parent_path), "w")
        f.close()
        # Debug: Print if the file is created
        # print("Parking lot list created!")
    else:
        # Debug: Print if the file existed
        # print("Parking lot list already existed!")
        pass

    if not path.isfile(parent_path + "/add_temporary_parking_lot.txt"):
        f_add_temp_parking_lot = open("{}/add_temporary_parking_lot.txt".format(parent_path), "w")
        f_add_temp_parking_lot.close()
        # Debug: Print if the file is created
        # print("Need to add parking lots container created!")
    else:
        # Debug: Print if the file existed
        # print("Need to add parking lots container already existed!")
        pass


# Create required working files
def file_manip(parent_path, input_name):                # Making log files for future analysis
    os.chdir("{}/data_process/{}".format(parent_path, input_name))

    # Debug: Print working directory
    # print(parent_path)

    def file_make(file_name):
        if not path.isfile(file_name):
            f = open(file_name, "w")
            f.close()
            # print(file_name + ' created!')
        else:
            # print(file_name + ' existed!')
            pass

    # Create files to store debug data
    file_make("debug.txt")
    file_make("defined_parking_lot.txt")
    file_make("landmarks.txt")
    file_make("parking_slots.txt")
    file_make("roi.txt")
    # file_make("avail_parking_lot.txt")

    # Create files to store parking lot data
    # os.chdir("./log_files")
    # file_make("01_std_log.csv")
    # file_make("02_org_log.csv")
    # file_make("03_calib_log.csv")

    os.chdir(parent_path)


# Open available parking lot file, append positions to a list
def file_open_avail_parking_lot(parent_path):
    # Initiate values
    file_flag = False
    avail_parking_lot = []

    # Open file contains defined parking lot name
    # Avoid using static addresses
    f_avail_parking_lot = open(parent_path + "/data_process/available_parking_lot.txt", 'r+')
    if os.stat(parent_path + "/data_process/available_parking_lot.txt").st_size == 0:
        # Indicates if the parking lot is defined or not. If not, halt the processing program
        file_flag = True  # Not defined value
        avail_parking_lot = ""
        return avail_parking_lot, file_flag
    else:
        string_x = ""
        # Initiate new list, get the value from the list
        lis = [line.split() for line in f_avail_parking_lot]
        # print(lis)
        file_length = len(lis)

        for ii in range(file_length):
            flag_multiple_white_space = len(lis[ii])
            if flag_multiple_white_space > 1:
                temp = ' '.join(lis[ii])
                string_x = temp
            else:
                for val in lis[ii]:
                    # Debug:
                    # print(val)
                    string_x = val
            avail_parking_lot.append(string_x)
    f_avail_parking_lot.close()

    return avail_parking_lot, file_flag


# Add new parking lot to the monitoring file
def file_append_avail_parking_lot(parent_path, new_parking_lot_name):
    # Initiate values:
    # Avoid using static addresses
    f_avail_parking_lot = open("{}/data_process/available_parking_lot.txt".format(parent_path), 'a+')
    f_avail_parking_lot.write(new_parking_lot_name)
    f_avail_parking_lot.write("\n")
    f_avail_parking_lot.close()


def file_append(parent_path, input_name, destination, name_of_file, string):
    f_append_file = open("{}/data_process/{}/{}/{}".format(parent_path,
                                                               input_name,
                                                               destination,
                                                               name_of_file), '+a')
    f_append_file.write(string)
    f_append_file.write("\n")
    f_append_file.close()


def file_clear_contents(parent_path, input_name, name_of_file):
    f_clear_file = open("{}/data_process/{}/log_files/{}".format(parent_path, input_name, name_of_file), 'w+')
    f_clear_file.close()


def file_clear_specific_content(parent_path, file_destination, delete_string):
    file_path = "{}/data_process/{}".format(parent_path, file_destination)
    delete_string = delete_string + "\n"
    with open(file_path, "r+") as f_delete_spec_content:
        read_content = f_delete_spec_content.readlines()
        f_delete_spec_content.seek(0)
        for line in read_content:
            if line != delete_string and line != "\n":
                f_delete_spec_content.write(line)
        f_delete_spec_content.truncate()


def check_defined_parking_lot(parent_path, input_name):
    defined_flag = False
    file_path = "{}/data_process/{}/defined_parking_lot.txt".format(parent_path, input_name)
    if os.stat(file_path).st_size != 0:
        defined_flag = True
    else:
        pass

    return defined_flag


def write_data_to_log_file(parent_path, input_name, name_of_file, input_string):
    file_path = parent_path + "/data_process/{}/log_files/{}".format(input_name, name_of_file)
    if os.stat(file_path).st_size == 0:
        file = open(file_path, 'a+')
        file.write("Image name,x1,y1,x2,y2,x3,y3,x4,y4\n")
        file.close()
    file = open(file_path, 'a+')
    file.write(input_string)
    file.close()


def get_time_stamp():
    current_time = "{}".format(dt.now())
    time_string = (current_time.split(".")[0]).split(" ")[0] + "-" + \
                  ((current_time.split(".")[0]).split(" ")[1]).split(":")[0] + "-" + \
                  ((current_time.split(".")[0]).split(" ")[1]).split(":")[1] + "-" + \
                  ((current_time.split(".")[0]).split(" ")[1]).split(":")[2]

    return time_string


# Remove spacing character in string
def file_name_modify(string):
    # Remove white spaces: " "
    modded_string = string.split(" ")
    result_string = "".join(modded_string)
    # Remove hyphen: "-"
    modded_string = result_string.split("-")
    result_string = "".join(modded_string)
    # Remove underscore: "_"
    modded_string = result_string.split("_")
    result_string = "".join(modded_string)

    return result_string


# Remove all folder content before another run, to avoid image show errors
# A better approach to file management is recommended. Deleting files is not recommended.
def remove_folder_content(address):
    for filename in os.listdir(address):
        if path.exists(path.join(address, filename)) & path.isfile(path.join(address, filename)):
            os.remove(path.join(address, filename))


# Remove all contents under a directory & the directory itself
def remove_all_contents(address):
    while True:
        # List all folders & files under the directory
        # Put in check under a loop through all item listed
        for filename in os.listdir(address):
            # If the item is a directory
            if path.isdir(path.join(address, filename)):
                # Check if the directory is empty
                # or check the list of item under the directory = 0
                if len(os.listdir(path.join(address, filename))) == 0:
                    # If yes, safe to remove the directory
                    os.rmdir(path.join(address, filename))
                else:
                    # If not, recurse the function
                    # The top directory is now the current item being checked
                    remove_all_contents(path.join(address, filename))
            else:
                # If the item is a file
                # Save to remove the file
                os.remove(path.join(address, filename))
        # Check if the original directory is empty or not
        if len(os.listdir(address)) == 0:
            # If yes, break the removing loop
            break
    # Remove the original top address
    os.rmdir(address)


# Get image name from image path
def get_image_name(image_path):
    image_name_list = image_path.split("/")
    image_name_list_length = len(image_name_list)

    return image_name_list[image_name_list_length - 1]