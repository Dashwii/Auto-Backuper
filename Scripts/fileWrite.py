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
                    print("")
                    print(f"Directory \"{directory}\" already in source directories")
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
                    print(f"Directory \"{self.directory}\" already in destination directories")
                    return
            with open("Destinations.txt", "a") as fileappender:
                fileappender.write("\n")
                fileappender.write(self.directory)
                print(f"Wrote \"{self.directory}\" to Directories.txt")
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
