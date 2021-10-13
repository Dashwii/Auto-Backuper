import re
import os


def get_path_name_list(directory="", sources_grab=False, destinations_grab=False):
    """
    :param directory:
    :param sources_grab:
    :param destinations_grab:
    :return list_of_path_names:

    Function will use re.split() to split a directory into names in a list based on it's path. The splitter will be
    either "/" or "\". This is used to get the true path of a directory no matter if "/" or "\" is used. Used mainly to
    bypass Tkinter's browse button using "/" for file paths. Can be used simply to split into path names. Or loop over
    a text file and gather all directory names inside of it using either "sources_grab" or "destinations_grab".
    """

    if sources_grab:
        lines = read_lines_from_file("Sources.txt")
        list_of_path_names = [re.split(r"[\\/]", line.strip()) for line in lines if line.strip() != "SOURCE DIRECTORIES:"]
        return list_of_path_names
    elif destinations_grab:
        lines = read_lines_from_file("Destinations.txt")
        list_of_path_names = [re.split(r"[\\/]", line.strip()) for line in lines if line.strip() != "DESTINATION DIRECTORIES:"]
        return list_of_path_names
    else:
        list_of_path_names = re.split(r"[\\/]", directory)
        return list_of_path_names


def remove_stickied_directory(directory):
    lines = read_lines_from_file("AutoSettings.txt")
    false_directory_index = lines.index(f"{directory}\n")
    lines[false_directory_index] = "\n"
    write_lines_to_file("AutoSettings.txt", lines)


def remove_written_directory_from_file(source_or_destination, directory):
    lines = read_lines_from_file(source_or_destination)
    directory_index = 0
    for i, line in enumerate(lines):
        if line.strip() == directory:
            lines[i] = ""
            directory_index = i

    # Check if lines has an index entry greater than directory_index.
    if directory_index + 1 > len(lines) - 1:
        lines[directory_index - 1] = lines[directory_index - 1].strip()
    write_lines_to_file(source_or_destination, lines)


# Sources
def source_directory_file_write(directory):
    # Check if names of the file path are in Sources.txt
    path_list_names = get_path_name_list(sources_grab=True)
    directory_path_list = get_path_name_list(directory=directory)
    # If the list of path names in the passed directory is in directory_path_lists then print that it's already written
    # and return.
    if directory_path_list in path_list_names:
        return
    append_directory_to_file("Sources.txt", directory)


def source_directories_list():
    # Gather directories from Sources.txt to show in source history button.
    source_directories = []
    lines = read_lines_from_file("Sources.txt")
    for line in lines:
        if line.strip() == "SOURCE DIRECTORIES:":
            continue
        else:
            directory = line.strip()
            source_directories.append(directory)
    if len(source_directories) == 0:
        source_directories.append("Copy a file from a source for it to be in your history")
    return source_directories


# Destinations
def destination_directory_file_write(directory):
    # Check if names of the file path are in Destination.txt
    directory_paths_list = get_path_name_list(directory=directory)
    list_of_written_destination_path_names = get_path_name_list(destinations_grab=True)
    # If the list of path names in the passed directory is in directory_path_lists then print that it's already written
    # and return.
    if directory_paths_list in list_of_written_destination_path_names:
        return
    append_directory_to_file("Destinations.txt", directory)


def destination_directories_list():
    # Gather directories from Destinations.txt to show in destinations history button.
    destination_directories = []
    lines = read_lines_from_file("Destinations.txt")
    for line in lines:
        if line.strip() == "DESTINATION DIRECTORIES:":
            continue
        else:
            directory = line.strip()
            destination_directories.append(directory)
    if len(destination_directories) == 0:
        destination_directories.append("Copy to a directory for it to be added to your history")
    return destination_directories


def read_lines_from_file(file_name):
    with open(f"{file_name}", "r") as file:
        lines = file.readlines()
    return lines


def write_lines_to_file(file_name, lines):
    with open(f"{file_name}", "w") as file:
        file.writelines(lines)
    return


def append_directory_to_file(file_name, directory):
    with open(file_name, "a") as file:
        file.seek(0, os.SEEK_END)
        file.write("\n")
        file.write(directory)
        print(f"Directory \"{directory}\" written into {file_name}")
