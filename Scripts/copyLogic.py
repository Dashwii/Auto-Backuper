import os
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
    file_name = ""
    temp_name = []
    origin_directory = list(reversed(list(origin_directory)))

    for i in origin_directory:
        if i == "\\" or i == "/":
            break
        else:
            temp_name.append(i)

    for i in list(reversed(temp_name)):
        i = str(i)
        file_name += i

    return file_name


def give_new_name(file_name, date, time_stamp):
    new_file_name = f"{file_name} {date} {time_stamp}"
    return new_file_name


def new_directory(destination_directory, file_name):
    new_dir = rf"{destination_directory}\{file_name}"
    os.mkdir(new_dir)
    return new_dir


def copy_to_directory(origin_dir, destination_dir, file_name):
    try:
        new_file_name = give_new_name(file_name, get_date(), get_timestamp())
        folder_dir = rf"{destination_dir}\{new_file_name}"
        shutil.copytree(origin_dir, folder_dir)
        print("File copied")
    except Exception as e:
        print(f"[ERROR], {e}")
    return


