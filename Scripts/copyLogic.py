import shutil
import datetime


def convert_backslashes_to_forwardslashes(path):
    # For any time of work with directories convert backslashes to forward slashes for compatibility on multiple OS's.
    string = ""
    for i in path:
        if i == "/":
            string += "".join("\\")
        else:
            string += "".join(i)
    return string


def get_timestamp():
    time_stamp = str(datetime.datetime.now().time().replace(microsecond=0))
    time_stamp = time_stamp.replace(":", "꞉")
    return time_stamp


def get_date():
    date = str(datetime.date.today())
    return date


def get_file_name(origin_directory):
    temp_name = ""
    for i in reversed(origin_directory):
        if i == "\\" or i == "/":
            break
        else:
            temp_name += i
    file_name = "".join([char for char in reversed(temp_name)])
    return file_name


def copy_to_directory(origin_dir, destination_dir, file_name):
    origin_dir = convert_backslashes_to_forwardslashes(origin_dir)
    destination_dir = convert_backslashes_to_forwardslashes(destination_dir)
    try:
        new_file_name = f"{file_name} {get_date()} {get_timestamp()}"
        folder_dir = rf"{destination_dir}/{new_file_name}"
        shutil.copytree(origin_dir, folder_dir)
        print(f"\nFile \"{new_file_name}\" copied to \"{destination_dir}\"")
    except Exception as e:
        print(f"\n[ERROR], {e}")
