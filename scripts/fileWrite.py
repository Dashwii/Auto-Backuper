import os
import json


class Settings:
    def __init__(self):
        self.settings_path = r"..\config\settings.json"
        if not os.path.exists(self.settings_path):
            self.create_settings()
        with open(self.settings_path, "r") as json_file:
            self.settings = json.load(json_file)


    def save_json(self):
        with open(self.settings_path, "w") as json_file:
            data = json.dumps(self.settings, indent=2, default=str)
            json_file.write(data)

    def create_settings(self):
        data = json.loads("""
{
  "Sources History": [],
  "Destinations History": [],
  "Settings": {
    "Stickied Source": [
      ""
    ],
    "Stickied Destinations": [
      "",
      "",
      "",
      ""
    ],
    "Auto Copy": [
      -1,
      false
    ],
    "Auto Delete": [
      -1,
      false
    ],
    "Auto Close": [
      -1,
      false
    ],
    "Last Auto Copy": false,
    "Google Upload": false,
    "Manual Copy Upload": false,
    "Google Folder ID": false
  }
}
""")
        with open(self.settings_path, "w") as settings:
            json.dump(data, settings, indent=2, default=str)


loaded_settings = Settings()


def remove_stickied_directory(directory, source_or_destination):
    if source_or_destination == "source":
        directories = loaded_settings.settings["Settings"]["Stickied Sources"]
    elif source_or_destination == "destination":
        directories = loaded_settings.settings["Settings"]["Stickied Destinations"]
    for saved_directory in directories:
        if saved_directory == directory:
            del directories[directories.index(saved_directory)]
    loaded_settings.save_json()


def remove_written_directory_from_file(source_or_destination, directory):
    if source_or_destination == "source":
        directories = loaded_settings.settings["Sources History"]
    elif source_or_destination == "destination":
        directories = loaded_settings.settings["Destinations History"]
    for saved_directory in directories:
        if saved_directory == directory:
            del directories[directories.index(saved_directory)]
    loaded_settings.save_json()


# Sources
def source_directory_file_write(directory):
    # Split path into names and compare those names with paths already in json file. This is for when there is a mix
    # of both forwardslashes and backslashes used in directory comparison.
    split_directory = os.path.normpath(directory).split(os.path.sep)
    split_saved_directories = [os.path.normpath(directory).split(os.path.sep) for directory in loaded_settings.settings["Sources History"]]
    if split_directory in split_saved_directories:
        return
    loaded_settings.settings["Sources History"].append(directory)
    loaded_settings.save_json()


def source_directories_list():
    sources = loaded_settings.settings["Sources History"]
    if len(sources) == 0:
        source_directories = ["Copy from a directory for it to be added to your history!"]
    else:
        source_directories = [directory for directory in sources]
    return source_directories


# Destinations
def destination_directory_file_write(directory):
    # Split path into names and compare those names with paths already in json file. This is for when there is a mix
    # of both forwardslashes and backslashes used in directory comparison.
    split_directory = os.path.normpath(directory).split(os.path.sep)
    split_saved_directories = [os.path.normpath(directory).split(os.path.sep) for directory in loaded_settings.settings["Destinations History"]]
    if split_directory in split_saved_directories:
        return
    loaded_settings.settings["Destinations History"].append(directory)
    loaded_settings.save_json()


def destination_directories_list():
    destinations = loaded_settings.settings["Destinations History"]
    if len(destinations) == 0:
        destination_directories = ["Copy to a directory for it to be added to your history"]
    else:
        destination_directories = [directory for directory in destinations]
    return destination_directories
