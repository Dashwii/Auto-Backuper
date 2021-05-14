import shutil
import datetime


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


def give_new_name(file_name, date, time_stamp):
    new_file_name = f"{file_name} {date} {time_stamp}"
    return new_file_name


def copy_to_directory(origin_dir, destination_dir, file_name):
    try:
        new_file_name = give_new_name(file_name, get_date(), get_timestamp())
        folder_dir = rf"{destination_dir}\{new_file_name}"
        shutil.copytree(origin_dir, folder_dir)
        print("\nFile copied")
    except Exception as e:
        print(f"[ERROR], {e}")
    return
