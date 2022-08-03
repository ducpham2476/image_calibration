import os
import yaml


# Check the configuration files
def write_default_configurations(parent):
    default_config_path = "{}/data_process/default_config.yaml".format(parent)

    if not os.path.isfile(default_config_path) or os.stat(default_config_path).st_size == 0:
        with open(default_config_path, 'w') as f_config:
            data = [
                {'configuration': 'default'},
                {'username': 'admin'},
                {'password': 'bk123456'},
                {'ip': '192.168.0.105'},
                {'port': 554},
                {'device number': '01'},
                {'delay time': 5},
                {'test calibration': False},
                {'write debug info': False},
                {'debug file location': '{}/data_process/debug'.format(parent)}
                ]
            yaml.dump(data, f_config)
        return True

    return False


# Check configuration files' conditions, return the state of those config files
# If the file does not exist, or if it contains no content, return False
# Else if the file exist and there are configurations within, return True
def check_configurations(parent):
    default_config_flag = False
    user_config_flag = False

    default_config_path = "{}/data_process/default_config.yaml".format(parent)
    user_config_path = "{}/data_process/user_config.yaml".format(parent)
    if os.path.isfile(default_config_path) and os.stat(default_config_path).st_size != 0:
        default_config_flag = True
    if os.path.isfile(user_config_path) and os.stat(user_config_path).st_size != 0:
        user_config_flag = True

    return default_config_flag, user_config_flag


# Get the configuration data from configuration files
def get_configurations(parent):
    # Check the configuration files condition
    default_flag, user_flag = check_configurations(parent)
    # print(default_flag, user_flag)
    # The user defined configuration has a higher priority, if it is defined then choose the user defined parameters
    # Else if the user configuration has not been defined, use the default configurations
    if user_flag:
        config_type = "user"
    elif not user_flag and default_flag:
        config_type = "default"
    else:
        return None
    # Based on the configuration type, get configuration file location
    if config_type == "default":
        config_location = "{}/data_process/default_config.yaml".format(parent)
    elif config_type == "user":
        config_location = "{}/data_process/user_config.yaml".format(parent)
    else:
        return None
    with open(config_location) as f_config:
        data = yaml.load(f_config, Loader=yaml.FullLoader)

    return data


# If the user decided to reset the configuration file, clear the user configuration file
def clear_configurations(parent):
    user_config_path = "{}/data_process/user_config.yaml".format(parent)
    f_config = open(user_config_path, 'w+')
    f_config.close()

    return


# Save user configurations to user config file
def write_user_configurations(parent, data):
    # If the input data is empty, return False to raise error
    if data is None:
        return
    # Get user configuration destination for file writing
    user_config_path = "{}/data_process/user_config.yaml".format(parent)
    # Get input data and convert into dictionary type
    with open(user_config_path, 'w') as f_config:
        write_data = [
            {'configuration': 'user'},
            {'username': data[1]['username']},
            {'password': data[2]['password']},
            {'ip': data[3]['ip']},
            {'port': data[4]['port']},
            {'device number': data[5]['device number']},
            {'delay time': data[6]['delay time']},
            {'test calibration': data[7]['test calibration']},
            {'write debug info': data[8]['write debug info']},
            {'debug file location': data[9]['debug file location']}
        ]
        # Write data to user configuration file
        yaml.dump(write_data, f_config)

        return True


# Test code
# parent = os.path.dirname(os.getcwd())
# print(parent)
#
# data = get_configurations(parent)
# print(data)
#
# input_data = []
# input_data.append('user')
# input_data.append('administrator')
# input_data.append('bk12345678')
# input_data.append('192.168.0.1')
# input_data.append(554)
# input_data.append('01')
# input_data.append(5),
# input_data.append(False)
# input_data.append(False)
# input_data.append(os.getcwd())
# print(len(input_data))
#
# print(write_user_configurations(parent, input_data))
# clear_configurations(parent)
# data = get_configurations(parent)
# print(data)
#
# print(write_default_configurations(parent))
# data = get_configurations(parent)
# print(data)
# print(type(data[7]['test calibration']))
# data[7]['test calibration'] = True
# print(data[7]['test calibration'])
# print(type(data[0]['configuration']))

# if type(data[0]['configuration']) is str:
#     print(0)
# else:
#     print(-1)