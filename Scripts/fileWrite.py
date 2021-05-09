class Sources:
    def __init__(self, directory):
        self.directory = directory

    @staticmethod
    def check_sources_len():
        len_of_lines = 0
        with open("Sources.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == "SOURCE DIRECTORIES:":
                    continue
                else:
                    len_of_lines += 1
        return len_of_lines

    @staticmethod
    def source_directory_file_write(directory):
        with open("Sources.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == directory:
                    print("Directory already in source directories")
                    return
            with open("Sources.txt", "a") as fileappender:
                fileappender.write("\n")
                fileappender.write(directory)
                print(f"Wrote {directory} to Sources.txt")
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
    def __init__(self, directory):
        self.directory = directory

    @staticmethod
    def check_destinations_len():
        len_of_lines = 0
        with open("Destinations.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == "DESTINATION DIRECTORIES:":
                    continue
                else:
                    len_of_lines += 1
        return len_of_lines


    def destination_directory_file_write(self):
        with open("Destinations.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == self.directory:
                    print("Directory already in source directories")
                    return
            with open("Destinations.txt", "a") as fileappender:
                fileappender.write("\n")
                fileappender.write(self.directory)
                print(f"Wrote {self.directory} to Directories.txt")
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






# def directory_file_write(directory, source_or_dest):
#     """Checks through every line, in the destinations file.
#        If the copied directories aren't in the file then they
#        are appended."""
#     if source_or_dest == "SOURCE":
#         print(f"Source: {directory}")
#         with open("Sources.txt", "r") as file:
#             lines = file.readlines()
#             if directory not in lines:
#                 with open("Sources.txt", "a") as fileappender:
#                     fileappender.write("\n")
#                     fileappender.write(directory)
#     else:
#         print(f"Destination {directory}")
#         with open("Destinations.txt", "r") as file:
#             lines = file.readlines()
#             if directory not in lines:
#                 with open("Destinations.txt", "a") as fileappender:
#                     fileappender.write("\n")
#                     fileappender.write(directory)
#             else:
#                 print("Directory already in history")
#
#
# # Used to add directories to a list of options for destinations history button
# def add_directories_to_list(source_history_or_destination_history):
#     """Checks destinations or sources text file depending on variable adds all lines that
#        to a list have a length > 0 for use for their corresponding history button."""
#     # Return sources list
#     if source_history_or_destination_history == "SOURCE":
#         source_history = []
#         with open("Sources.txt", "r") as file:
#             lines = file.readlines()
#             for line in lines:
#                 if len(line.strip()) == 0 or line.strip() == "SOURCES:":
#                     continue
#                 else:
#                     source_history.append(line.strip())
#             if len(source_history) == 0:
#                 source_history.append("Put in a source for it to be added to your history!")
#             return source_history
#     # Return destinations list
#     else:
#         directory_history = []
#         with open("Destinations.txt", "r") as file:
#             lines = file.readlines()
#             for line in lines:
#                 if len(line.strip()) == 0 or line.strip() == "DIRECTORIES:":
#                     continue
#                 else:
#                     directory_history.append(line.strip())
#             if len(directory_history) == 0:
#                 directory_history.append("Copy folders to destinations to add them to your history!")
#         return directory_history
