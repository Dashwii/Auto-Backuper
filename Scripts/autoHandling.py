import os
from datetime import datetime as dt
from send2trash import send2trash
from copyLogic import *
from fileWrite import read_lines_from_file, write_lines_to_file, remove_stickied_directory


# Auto Deletion
def check_files_then_delete(directories):
    settings_lines = read_lines_from_file("AutoSettings.txt")
    days_until_delete = int(settings_lines[5].strip())
    delete_permission = settings_lines[6].strip()
    if days_until_delete == -1 or delete_permission == "NO":
        return

    directories_list = [convert_backslashes_to_forwardslashes(directory) for directory in directories]
    if len(directories_list) == 0:
        print("[Auto Delete] You're trying to run auto delete without any stickied directories. Add a directory to the "
              "one of the destination paths, then click \"Stick Directories\" for auto delete to work.")
        return
    print("Checking for old files...")
    files_were_deleted = delete_old_files_in_directories(directories_list, days_until_delete)
    if not files_were_deleted:
        print("No files deleted!")


def delete_old_files_in_directories(directories, max_age):
    # Loops through files in each directory. If the file is older than the max age given, then it is deleted.
    files_deleted_check = False
    blacklisted_files_warning = False
    for directory in directories:
        try:
            file_list = os.listdir(directory)
        except FileNotFoundError as e:
            print(e)
            print(f"[Auto Delete] Stickied destination directory \"{directory}\" not found. Removing from stickied "
                  f"directories.")
            remove_stickied_directory(directory)
            continue
        for file in file_list:
            # Prevent files that were not copied from the program from being deleted.
            if "꞉" not in file:
                blacklisted_files_warning = True
                continue
            else:
                file_path = os.path.join(directory, file)
                # Time comparisons
                file_date = dt.fromtimestamp(os.path.getctime(file_path)).date()
                time_passed = dt.today().date() - file_date

                if time_passed.days >= max_age:
                    send2trash(file_path)
                    print(f"File: '{file_path}' is {time_passed.days} days old. It has been sent to the recycle bin.\n")
                    files_deleted_check = True
    if blacklisted_files_warning:
        print("[Auto Delete] There were files that were ignored in the directory you are auto deleting from. "
              "Recommend creating a specific folders for copies to prevent deletion mistakes in the future.\n")
    return files_deleted_check


# Auto Copy
def write_run_date():
    latest_auto_copy = dt.today().date()
    lines = read_lines_from_file("AutoSettings.txt")
    lines[13] = f"{latest_auto_copy}\n"
    write_lines_to_file("AutoSettings.txt", lines)


def compare_date():
    lines = read_lines_from_file("AutoSettings.txt")
    last_auto_copy_date = lines[13].strip()
    # Return false if last_run_date is not written
    if len(last_auto_copy_date) == 0:
        return False

    present = dt.today().date()
    past = dt.strptime(last_auto_copy_date, "%Y-%m-%d")
    past = dt.date(past)

    days_since_copy = present - past
    days_since_copy = days_since_copy.days
    return int(days_since_copy)


def auto_copy_execute(source, destinations, file_name):
    lines = read_lines_from_file("AutoSettings.txt")
    auto_copy_permission = lines[2].strip()
    auto_copy_freq = int(lines[1].strip())
    days_since_copy = compare_date()

    if auto_copy_freq == -1 or auto_copy_permission == "NO":
        return
    if len(source) == 0 or len(destinations) == 0:
        print("[Auto Copy] You're trying to run auto copy without any stickied directories. Add a directory to the "
              "source and destination paths, then click \"Stick Directories\" for auto copy to work.")
        return
    if not os.path.exists(source):
        print("[Auto Copy] FileNotFoundError")
        print(f"Stickied source \"{source}\" not found. Removing it from stickied directories.")
        remove_stickied_directory(source)
        return
    # If days_since_copy equals False. Then it must be the first time auto copy is running. Write date to prevent error.
    if not days_since_copy:
        write_run_date()
        days_since_copy = compare_date()

    if days_since_copy >= auto_copy_freq:
        print("Executing Auto Run")
        for directory in destinations:
            if not os.path.exists(directory):
                print(f"Directory \"{directory}\" does not exist. Removed from stickied directories.")
                remove_stickied_directory(directory)
                continue
            copy_to_directory(source, directory, file_name)
        write_run_date()
    else:
        print("Not running auto copy\n")
