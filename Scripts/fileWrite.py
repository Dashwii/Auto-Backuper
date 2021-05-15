import re
import os


def get_path_name_list(directory="", sources_grab=False, destinations_grab=False):
    """
    :param directory:
    :param sources_grab:
    :param destinations_grab:
    :return path_list_name:

    Function will use re.split() to split a directory into names in a list based on it's path. The splitter will be
    either "/" or "\". This is used to get the true path of a directory no matter if "/" or "\" is used. Used mainly to
    bypass Tkinter's browse button using "/" for file paths. Can be used simply to split into path names. Or loop over
    a text file and gather all directory names inside of it using either "sources_grab" or "destinations_grab".
    """

    if sources_grab:
        with open("Sources.txt", "r") as sources_file:
            lines = sources_file.readlines()
        path_list_name = [re.split(r"[\\/]", line) for line in lines if line.strip() != "SOURCE DIRECTORIES:"]
        return path_list_name
    elif destinations_grab:
        with open("Destinations.txt", "r") as destinations_file:
            lines = destinations_file.readlines()
        path_list_name = [re.split(r"[\\/]", line) for line in lines if line.strip() != "DESTINATION DIRECTORIES:"]
        return path_list_name
    else:
        path_list_name = re.split(r"[\\/]", directory)
        return path_list_name


class Sources:
    @staticmethod
    def source_directory_file_write(directory):
        with open("Sources.txt", "a") as file:
            path_list_names = get_path_name_list(sources_grab=True)
            directory_path_list = get_path_name_list(directory=directory)
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
    def delete_false_source(directory):
        directory_path_list = get_path_name_list(directory=directory)
        with open("Sources.txt", "r") as file:
            lines = file.readlines()
            with open("Sources.txt", "w") as file_write:
                for count, line in enumerate(lines):
                    dir_line = get_path_name_list(directory=line.strip())
                    if dir_line == directory_path_list:
                        lines[count] = ""
                        file_write.writelines(lines)
                        print(f"Directory \"{directory}\" deleted from Sources.txt")
                        return
                file_write.writelines(lines)
                print(f"Directory \"{directory}\" does not exist.")
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
        with open("Destinations.txt", "a") as file:
            path_list_names = get_path_name_list(destinations_grab=True)
            directory_path_names = get_path_name_list(directory=directory)
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
