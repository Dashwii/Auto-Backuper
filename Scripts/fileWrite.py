import re
import os


class Sources:
    @staticmethod
    def source_directory_file_write(directory):
        """
        Function will use re.split() to take each path name and put it into a list. Function uses re.split on directory
        given and will compare to see if it is in the list of path_list_names. This method is used because it bypasses
        the problem of Tkinter using "/" for file paths instead of "\". The same directory will not be written twice,
        regardless of slashes used for its path.
        """
        with open("Sources.txt", "a+") as file:
            file.seek(0)
            source_directories = file.readlines()
            path_list_names = [re.split(r"[\\/]", line.strip())
                               for line in source_directories if line.strip() != "SOURCE DIRECTORIES:"]
            directory_path_list = re.split(r"[\\/]", directory)
            if directory_path_list in path_list_names:
                print(f"\nDirectory \"{directory}\" already in Sources.txt")
                return
            else:
                file.seek(0, os.SEEK_END)
                file.write("\n")
                file.write(directory)
                print(f"\nDirectory \"{directory}\" written into Sources.txt")
                return

    @staticmethod
    def source_directories_list():
        source_directories = []
        with open("Sources.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == "SOURCE DIRECTORIES:":
                    continue
                else:
                    directory = line.strip()
                    source_directories.append(directory)
            if len(source_directories) == 0:
                source_directories.append("Copy a file from a source for it to be in your history!")
        return source_directories


class Destinations:
    @staticmethod
    def destination_directory_file_write(directory):
        """
        Function will use re.split() to take each path name and put it into a list. Function uses re.split on directory
        given and will compare to see if it is in the list of path_list_names. This method is used because it bypasses
        the problem of Tkinter using "/" for file paths instead of "\". The same directory will not be written twice,
        regardless of slashes used for its path.
        """
        with open("Destinations.txt", "a+") as file:
            file.seek(0)
            destination_directories = file.readlines()
            path_list_names = [re.split(r"[\\/]", line.strip())
                               for line in destination_directories if line.strip() != "DESTINATION DIRECTORIES:"]
            directory_path_names = re.split(r"[\\/]", directory)
            if directory_path_names in path_list_names:
                print(f"Directory \"{directory}\" already in Destinations.txt")
                return
            else:
                file.seek(0, os.SEEK_END)
                file.write("\n")
                file.write(directory)
                print(f"Directory \"{directory}\" written into Destinations.txt")
                return

    @staticmethod
    def destination_directories_list():
        destination_directories = []
        with open("Destinations.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == "DESTINATION DIRECTORIES:":
                    continue
                else:
                    directory = line.strip()
                    destination_directories.append(directory)
            if len(destination_directories) == 0:
                destination_directories.append("Copy to a directory for it to be added to your history!")
        return destination_directories
