import os
import copyLogic
from datetime import datetime as dt
import send2trash
from copyLogic import *


class AutoDelete:
    def check_files_then_delete(self):
        with open("Auto Settings.txt", "r") as file:
            lines = file.readlines()
            days_until_delete = lines[6].strip()
        if days_until_delete == "-1":
            return

        print("Checking for old files...")
        with open("Destinations.txt", "r") as directories_file:
            deleted_files = False
            lines = directories_file.readlines()
            try:
                for directory in lines:
                    if directory.strip() == "" or directory.strip() == "DESTINATION DIRECTORIES:":
                        continue
                    else:
                        deleted_files = self.check_directories(rf"{directory.strip()}", int(days_until_delete))
            except Exception as e:
                print("[ERROR]", e)
            if not deleted_files:
                print("No files deleted!")

    @staticmethod
    def check_directories(directory, day_delete):
        deleted_files = False
        try:
            for file_item in os.listdir(directory):
                file_date = dt.fromtimestamp(os.path.getctime(rf"{directory}\{file_item}")).date()
                present = dt.today().date()
                time_passed = present - file_date
                time_passed = time_passed.days
                if time_passed > day_delete:
                    print("")
                    print(rf"This file: [{directory}\{file_item}] is {time_passed} days old and will be deleted")
                    send2trash.send2trash(rf"{directory}\{file_item}")
                    deleted_files = True
                    print("Remove Completed")
        except Exception as e:
            print("[ERROR]", e)
            return
        return deleted_files


class AutoCopy:
    def __init__(self, source, source_file_name, *directories):
        self.source = source
        self.source_file_name = source_file_name
        self.directories = directories

    @staticmethod
    def write_run_date():
        latest_run = dt.today().date()
        with open("Auto Settings.txt", "r") as file:
            lines = file.readlines()
        lines[15] = f"{latest_run}\n"
        with open("Auto Settings.txt", "w") as file:
            file.writelines(lines)

    @staticmethod
    def compare_date():
        with open("Auto Settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines[15].strip()) == 0:
                return "No Date"
            else:
                last_run_date = lines[15].strip("\n")

            present = dt.today().date()
            past = dt.strptime(last_run_date, "%Y-%m-%d")
            past = dt.date(past)

            days_since_copy = present - past
            days_since_copy = days_since_copy.days
            return days_since_copy


    def auto_copy_execute(self):
        with open("Auto Settings.txt", "r") as file:
            lines = file.readlines()
        auto_copy_freq = lines[1].strip()
        if auto_copy_freq == "-1":
            return
        # If it is first time running auto copy. It will fail. The while True loop will allow the program to write a date
        # and try the auto run again.
        while True:
            try:
                if lines[2].strip() == "YES" and int(self.compare_date()) > int(auto_copy_freq):
                    print("Executing Auto Run")
                    for directory in self.directories:
                        try:
                            if directory.strip() == "DESTINATION DIRECTORIES:":
                                continue
                            else:
                                copyLogic.copy_to_directory(self.source, directory, self.source_file_name)
                        except Exception as e:
                            print("[ERROR]", e)
                            return
                    self.write_run_date()
                    return
                else:
                    print("Not running auto copy")
                    return
            except Exception as e:
                print(f"[ERROR], this is probably the first time autorun is running. Writing the run date.", e)
                self.write_run_date()
