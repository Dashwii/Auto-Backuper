import os
from datetime import datetime as dt
from send2trash import send2trash
from copyLogic import *
from fileWrite import remove_stickied_directory, loaded_settings
from fileUpload import upload_files_to_google, delete_old_gdrive_backups


# Auto Deletion
def check_files_then_delete(directories):
    settings_dict = loaded_settings.settings
    days_until_delete = settings_dict["Settings"]["Auto Delete"][0]
    state = settings_dict["Settings"]["Auto Delete"][1]
    if days_until_delete == -1 or not state:
        return
    directories_list = [convert_backslashes_to_forwardslashes(directory) for directory in directories]
    if len(directories_list) == 0:
        print("[Auto Delete] You're trying to run auto delete without any stickied directories. Add a directory to the "
              "one of the destination paths, then click \"Stick Directories\" for auto delete to work.")
        return
    print("\nChecking for old files on computer...")
    files_were_deleted = delete_old_files_in_directories(directories_list, days_until_delete)
    if not files_were_deleted:
        print("No files deleted!\n")
    if settings_dict["Settings"]["Google Upload"]:
        if not settings_dict["Settings"]["Google Folder ID"]:
            print("[Auto Delete] Please set a Google Folder ID of where you backups are!")
            return
        print("Checking for old files on Google drive...")
        delete_old_gdrive_backups(settings_dict["Settings"]["Google Folder ID"], days_until_delete)



def delete_old_files_in_directories(directories, max_age):
    max_age = int(max_age)
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
            remove_stickied_directory(directory, "destination")
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
              "Recommend creating a specific folder for copies to prevent deletion mistakes in the future.\n")
    return files_deleted_check


# Auto Copy
def write_run_date():
    latest_auto_copy = dt.today().date()
    loaded_settings.settings["Settings"]["Last Auto Copy"] = latest_auto_copy
    loaded_settings.save_json()


def compare_date():
    last_auto_copy_date = loaded_settings.settings["Settings"]["Last Auto Copy"]
    if not last_auto_copy_date:
        return False
    # Turn into string after if condition. (Doing this because if I turn the boolean into a str before
    # it won't be caught by the If condition, resulting in an error.)
    last_auto_copy_date = str(last_auto_copy_date)
    present = dt.today().date()
    past = dt.strptime(last_auto_copy_date, "%Y-%m-%d")
    past = dt.date(past)
    days_since_copy = present - past
    days_since_copy = days_since_copy.days
    return int(days_since_copy)


def online_upload(path, backup_folder_id):
    if not backup_folder_id:
        print("[ERROR] You're trying to upload files to Google drive without a target folder ID!")
        return
    upload_files_to_google(path, backup_folder_id)


def auto_copy_execute(source, destinations, file_name):
    auto_copy_freq = int(loaded_settings.settings["Settings"]["Auto Copy"][0])
    auto_copy_permission = loaded_settings.settings["Settings"]["Auto Copy"][1]
    days_since_copy = compare_date()
    if auto_copy_freq == -1 or not auto_copy_permission:
        return
    if len(source) == 0 or len(destinations) == 0:
        print("[Auto Copy] You're trying to run auto copy without any stickied directories. Add a directory to the "
              "source and destination paths, then click \"Stick Directories\" for auto copy to work.")
        return
    if not os.path.exists(source):
        print(f"Stickied source \"{source}\" not found. Removing it from stickied directories.")
        remove_stickied_directory(source, "source")
        return
    # If days_since_copy = False. Then it must be the first time auto copy is running. Write date to prevent error.
    if not days_since_copy:
        write_run_date()
        days_since_copy = compare_date()

    if days_since_copy >= auto_copy_freq:
        print("Running auto copy")
        for directory in destinations:
            if not os.path.exists(directory):
                print(f"Directory \"{directory}\" does not exist. Removed from stickied directories.")
                remove_stickied_directory(directory, "destination")
                continue
            copy_to_directory(source, directory, file_name)
        if loaded_settings.settings["Settings"]["Google Upload"]:
            print("\nUploading files to google drive...")
            try:
                online_upload(source, loaded_settings.settings["Settings"]["Google Folder ID"])
            except Exception as e:
                print(f"[ERROR]{e}")
        write_run_date()
    else:
        print("Not running auto copy")
        return
