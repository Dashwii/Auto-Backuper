import tkinter as tk
from tkinter import filedialog
from autoHandling import *
from fileWrite import *
import sys
import threading

LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 4)


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def close(self):
        self.destroy()


class MainPage(tk.Frame, GUI):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.copy_in_process = False

        # "Clipboard" saved directories
        self.saved_source_directory = ""
        self.saved_destination_directory = ""

        # "Clipboard" current saved directory for removal
        self.current_saved_removal_directory = ""

        # Settings
        show_settings_button = tk.Button(self, text="Settings",
                                         command=lambda: controller.show_frame(SettingsPage), padx=10, pady=2)
        show_settings_button.place(x=628, y=225)

        # Copy
        self.copy_button = tk.Button(self, text="Copy!",
                                     command=lambda: threading.Thread(target=self.execute_copies).start(), padx=80, pady=2)
        self.copy_button.place(x=256, y=225)

        # Stick Directories Button
        stick_button = tk.Button(self, text="Stick Directories",
                                 command=lambda: self.stick_directories(), padx=10, pady=2)
        stick_button.place(x=6, y=225)

        # Remove directory button
        remove_directory_button = tk.Button(self, text="Remove Directory",
                                            command=lambda: self.remove_directory_from_history(
                                                self.current_saved_removal_directory))
        remove_directory_button.place(x=597, y=18)
        # Source Path Entry
        source_path_label = tk.Label(self, text="Source Path", fg="grey")
        source_path_label.place(x=6, y=5)

        self.source_path_entry = tk.Entry(self)
        self.source_path_entry.insert(0, self.path_auto_insert_directory("source_1"))
        self.source_path_entry.bind("<FocusIn>", lambda event: self.copy_selected_directory_to_bar(self.source_path_entry))
        self.source_path_entry.place(x=8, y=25, height=22, width=363)

        # Source Browse Button
        source_path_browse = tk.Button(self, text="Browse", command=lambda: self.browse_paths(self.source_path_entry))
        source_path_browse.place(x=380, y=22)

        # Destination Path Entries
        self.destinations_paths_label = tk.Label(self, text="Destination Paths", fg="grey")
        self.destinations_paths_label.place(x=6, y=78)

        self.destination_path_entry1 = tk.Entry(self)
        self.destination_path_entry1.insert(0, self.path_auto_insert_directory(0))
        self.destination_path_entry1.bind("<FocusIn>",
                                          lambda event: self.copy_selected_directory_to_bar(self.destination_path_entry1))
        self.destination_path_entry1.place(x=8, y=100, height=22, width=363)

        self.destination_path_entry2 = tk.Entry(self)
        self.destination_path_entry2.insert(0, self.path_auto_insert_directory(1))
        self.destination_path_entry2.bind("<FocusIn>",
                                          lambda event: self.copy_selected_directory_to_bar(self.destination_path_entry2))

        self.destination_path_entry2.place(x=8, y=130, height=22, width=363)

        self.destination_path_entry3 = tk.Entry(self)
        self.destination_path_entry3.insert(0, self.path_auto_insert_directory(2))
        self.destination_path_entry3.bind("<FocusIn>",
                                          lambda event: self.copy_selected_directory_to_bar(self.destination_path_entry3))
        self.destination_path_entry3.place(x=8, y=160, height=22, width=363)

        self.destination_path_entry4 = tk.Entry(self)
        self.destination_path_entry4.insert(0, self.path_auto_insert_directory(3))
        self.destination_path_entry4.bind("<FocusIn>",
                                          lambda event: self.copy_selected_directory_to_bar(self.destination_path_entry4))
        self.destination_path_entry4.place(x=8, y=190, height=22, width=363)

        # Destination Browse Buttons
        destination_path_browse1 = tk.Button(self, text="Browse",
                                             command=lambda: self.browse_paths(self.destination_path_entry1))
        destination_path_browse1.place(x=380, y=97)

        destination_path_browse2 = tk.Button(self, text="Browse",
                                             command=lambda: self.browse_paths(self.destination_path_entry2))
        destination_path_browse2.place(x=380, y=127)

        destination_path_browse3 = tk.Button(self, text="Browse",
                                             command=lambda: self.browse_paths(self.destination_path_entry3))
        destination_path_browse3.place(x=380, y=157)

        destination_path_browse4 = tk.Button(self, text="Browse",
                                             command=lambda: self.browse_paths(self.destination_path_entry4))
        destination_path_browse4.place(x=380, y=187)

        # Source History Button
        source_directory_data = source_directories_list()
        self.source_variable_directory = tk.StringVar(controller)
        self.source_variable_directory.set("History")
        self.source_directory_history = tk.OptionMenu(self, self.source_variable_directory, *source_directory_data,
                                                      command=lambda x:
                                                      self.save_history_dir_to_variable(self.source_variable_directory))
        self.source_directory_history.place(x=430, y=18)

        # Destination History Button
        destination_directory_data = destination_directories_list()
        self.destination_variable_directory = tk.StringVar(controller)
        self.destination_variable_directory.set("History")
        self.destination_directory_history = tk.OptionMenu(self, self.destination_variable_directory,
                                                           *destination_directory_data,
                                                           command=lambda x: self.save_history_dir_to_variable(
                                                               self.destination_variable_directory))
        self.destination_directory_history.place(x=430, y=93)

        self.check_copying_process()

        # Auto Run Check
        self.auto_run_done = self.run_auto_check()

        # Auto close
        self.auto_close_state = loaded_settings.settings["Settings"]["Auto Close"][1]
        if self.auto_close_state and len(sys.argv) > 1:
            seconds = int(loaded_settings.settings["Settings"]["Auto Close"][0])
            if seconds < 0:
                seconds = 0
            print("")
            self.auto_close_app(seconds, controller)

    def check_copying_process(self):
        if self.copy_in_process and self.copy_button["state"] == "normal":
            self.copy_button["state"] = "disabled"
        elif not self.copy_in_process and self.copy_button["state"] == "disabled":
            self.copy_button["state"] = "normal"
        self.after(10, self.check_copying_process)

    def auto_close_app(self, second, controller):
        if not self.auto_close_state or sys.argv[1] != "auto":
            return
        if second < 1 and self.auto_run_done:
            controller.close()
        print(f"\rClosing in {second} seconds...", end="")
        self.after(1000, self.auto_close_app, second - 1, controller)

    def stick_directories(self):
        # Each entry bar is associated with an index key. The key's value will be saved in a list index for the
        # respective bar in settings.json.
        bars = {0: self.destination_path_entry1.get(), 1: self.destination_path_entry2.get(),
                2: self.destination_path_entry3.get(), 3: self.destination_path_entry4.get()}
        loaded_settings.settings["Settings"]["Stickied Source"][0] = self.source_path_entry.get()
        for destination in bars.keys():
            loaded_settings.settings["Settings"]["Stickied Destinations"][destination] = bars[destination]
        loaded_settings.save_json()

    @staticmethod
    def path_auto_insert_directory(caller):
        if caller == "source_1":
            return loaded_settings.settings["Settings"]["Stickied Source"][0]
        for index, directory in enumerate(loaded_settings.settings["Settings"]["Stickied Destinations"]):
            if caller == index:
                return directory

    def run_auto_check(self):
        auto_copy_execute(self.source_path_entry.get(), self.add_destination_directories_to_list(),
                          get_file_name(self.source_path_entry.get()))
        check_files_then_delete(self.add_destination_directories_to_list())
        return True

    def remove_directory_from_history(self, directory_passed):
        if (directory_passed == "Copy a file from a source for it to be in your history" or
                directory_passed == "Copy to a directory for it to be added to your history"):
            return
        if directory_passed in source_directories_list():
            remove_written_directory_from_file("source", directory_passed)
            self.current_saved_removal_directory = ""
        elif directory_passed in destination_directories_list():
            remove_written_directory_from_file("destination", directory_passed)
            self.current_saved_removal_directory = ""
        else:
            return

    def save_history_dir_to_variable(self, caller):
        # If the caller argument is source_variable_directory then the selected directory from source_variable_directory
        # will be saved into the "saved_source_directory" variable. If caller is one of the destination paths,
        # then the selected path will be saved into the "saved_destination_directory".
        if caller == self.source_variable_directory:
            if self.source_variable_directory.get() == "Copy a file from a source for it to be in your history":
                self.source_variable_directory.set("History")
            else:
                self.saved_source_directory = self.source_variable_directory.get()
                self.current_saved_removal_directory = self.source_variable_directory.get()
                self.source_variable_directory.set("History")
        else:
            if self.destination_variable_directory.get() == "Copy to a directory for it to be added to your history":
                self.destination_variable_directory.set("History")
            else:
                self.saved_destination_directory = self.destination_variable_directory.get()
                self.current_saved_removal_directory = self.destination_variable_directory.get()
                self.destination_variable_directory.set("History")

    def copy_selected_directory_to_bar(self, bar_name):
        # Function is passed a bar name, if the bar name is source_path_entry and the length of the saved_directory_directory
        # is greater than 0. Then the source bar contents will be deleted and the saved directory variable will be inserted.
        # Works the same for destination entries.
        destinations_entries = [self.destination_path_entry1, self.destination_path_entry2, self.destination_path_entry3,
                                self.destination_path_entry4]
        if bar_name == self.source_path_entry and len(self.saved_source_directory) > 0:
            self.source_path_entry.delete(0, "end")
            self.source_path_entry.insert(0, self.saved_source_directory)
            self.saved_source_directory = ""
        if bar_name in destinations_entries and len(self.saved_destination_directory) > 0:
            bar_name.delete(0, "end")
            bar_name.insert(0, self.saved_destination_directory)
            self.saved_destination_directory = ""

    def add_destination_directories_to_list(self):
        """Adds directories from get() to a list then returns it"""
        list_of_directories = [self.destination_path_entry1.get(), self.destination_path_entry2.get(),
                               self.destination_path_entry3.get(), self.destination_path_entry4.get()]
        # Remove empty destination paths from list
        list_of_directories = [i for i in list_of_directories if i != ""]
        return list_of_directories

    def execute_copies(self):
        list_of_destination_directories = self.add_destination_directories_to_list()
        source_directory = self.source_path_entry.get()
        if len(self.source_path_entry.get()) == 0:
            print("[ERROR] No source directory!")
            return
        if len(list_of_destination_directories) == 0:
            print("[ERROR] No destinations given!")
            return
        if not os.path.exists(source_directory):
            print(f"Source directory \"{source_directory}\" does not exist.")
            return
        for index, directory in enumerate(list_of_destination_directories[:]):
            if not os.path.exists(directory):
                print(f"Destination directory \"{directory}\" does not exist.")
                list_of_destination_directories.pop(index)
        self.copy_in_process = True
        source_directory_file_write(source_directory)
        # Loops over every dictionary in the list and copies the source to each directory
        for i in list_of_destination_directories:
            copy_to_directory(source_directory, i, get_file_name(source_directory))
            destination_directory_file_write(i)
        if loaded_settings.settings["Settings"]["Manual Copy Upload"]:
            online_upload(source_directory, loaded_settings.settings["Settings"]["Google Folder ID"])
        self.copy_in_process = False
        return True

    @staticmethod
    def browse_paths(path_entry_box):
        source_path = filedialog.askdirectory()
        if len(source_path) == 0:
            return
        path_entry_box.delete(0, "end")
        path_entry_box.insert(0, source_path)


class SettingsPage(tk.Frame, GUI):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        settings_label = tk.Label(self, text="Settings", font="LARGE_FONT")
        settings_label.pack(anchor="center")
        vcmd = (self.register(self.check_valid), "%P")

        # Back to main page
        back_home = tk.Button(self, text="Back",
                              command=lambda: controller.show_frame(MainPage), padx=10, pady=2)
        back_home.place(x=645, y=225)

        # Save Settings
        save_settings = tk.Button(self, text="Save",
                                  command=lambda: self.save_button(), padx=10, pady=2)
        save_settings.place(x=585, y=225)

        # Erase Settings
        erase_settings_button = tk.Button(self, text="Erase Settings", command=lambda: self.revert_settings(), padx=10,
                                          pady=2)
        erase_settings_button.place(x=475, y=225)

        # Saved Settings
        settings_dict = loaded_settings.settings["Settings"]
        # Auto Copy Checkbox State
        if settings_dict["Auto Copy"][1]:
            self.auto_copy_checkbox_state = tk.IntVar(value=1)
        else:
            self.auto_copy_checkbox_state = tk.IntVar(value=0)

        # Auto Delete Checkbox State
        if settings_dict["Auto Delete"][1]:
            self.auto_delete_checkbox_state = tk.IntVar(value=1)
        else:
            self.auto_delete_checkbox_state = tk.IntVar(value=0)

        # Auto Close Checkbox State
        if settings_dict["Auto Close"][1]:
            self.auto_close_checkbox_state = tk.IntVar(value=1)
        else:
            self.auto_close_checkbox_state = tk.IntVar(value=0)

        # Google Upload Checkbox State
        if settings_dict["Google Upload"]:
            self.google_upload_checkbox_state = tk.IntVar(value=1)
            if settings_dict["Manual Copy Upload"]:
                self.manual_google_upload_checkbox_state = tk.IntVar(value=1)
            else:
                self.manual_google_upload_checkbox_state = tk.IntVar(value=0)
        else:
            self.google_upload_checkbox_state = tk.IntVar(value=0)
            self.manual_google_upload_checkbox_state = tk.IntVar(value=0)

        # Auto Copy
        auto_copy_label = tk.Label(self, text="Auto Copy?", font="LARGE_FONT")
        auto_copy_label.place(x=0, y=40)

        auto_copy_checkbox = tk.Checkbutton(self, variable=self.auto_copy_checkbox_state)
        auto_copy_checkbox.place(x=90, y=40)

        copy_frequency_label = tk.Label(self, text="Enter auto copy frequency (Days):", font="LARGE_FONT")
        copy_frequency_label.place(x=0, y=70)

        self.copy_frequency_entry = tk.Entry(self, width=3, font="LARGE_FONT", validate="key", validatecommand=vcmd)
        self.copy_frequency_entry.place(x=240, y=73)

        # Auto Delete
        auto_delete_label = tk.Label(self, text="Auto Delete?", font="LARGE_FONT")
        auto_delete_label.place(x=500, y=40)

        auto_delete_checkbox = tk.Checkbutton(self, variable=self.auto_delete_checkbox_state)
        auto_delete_checkbox.place(x=600, y=40)

        delete_frequency_label = tk.Label(self, text="Delete after (Days):", font="LARGE_FONT")
        delete_frequency_label.place(x=500, y=70)

        self.delete_frequency_entry = tk.Entry(self, width=3, font="LARGE_FONT", validate="key", validatecommand=vcmd)
        self.delete_frequency_entry.place(x=642, y=73)

        # Auto Close
        auto_close_label = tk.Label(self, font="LARGE_FONT", text="Auto Close?")
        auto_close_label.place(x=500, y=120)
        auto_close = tk.Checkbutton(self, variable=self.auto_close_checkbox_state)
        auto_close.place(x=600, y=120)

        seconds_until_close_label = tk.Label(self, font="LARGE_FONT", text="Time until close:")
        seconds_until_close_label.place(x=500, y=150)

        self.seconds_until_close = tk.Entry(self, width=3, font="LARGE_FONT", validate="key", validatecommand=vcmd)
        self.seconds_until_close.place(x=618, y=152)

        # Auto Copy Entry Set
        if settings_dict["Auto Copy"][0] != -1:
            self.copy_frequency_entry.insert(0, settings_dict["Auto Copy"][0])

        # Auto Delete Entry Set
        if settings_dict["Auto Delete"][0] != -1:
            self.delete_frequency_entry.insert(0, settings_dict["Auto Delete"][0])

        # Auto Close Entry Set
        if settings_dict["Auto Close"][0] != -1:
            self.seconds_until_close.insert(0, settings_dict["Auto Close"][0])

        # Google upload
        google_upload_label = tk.Label(self, text="Google drive upload?", font="LARGE_FONT")
        google_upload_label.place(x=0, y=142)

        self.google_upload_checkbox = tk.Checkbutton(self, variable=self.google_upload_checkbox_state,
                                                     command=lambda: self.manual_google_copy_guard(self.google_upload_checkbox_state.get()))
        self.google_upload_checkbox.place(x=158, y=142)

        google_login_label = tk.Label(self, text="Enter target folder ID:", font="LARGE_FONT")
        google_login_label.place(x=0, y=200)

        manual_google_copying_label = tk.Label(self, text="Upload to google when copying manually?", font="LARGE_FONT")
        manual_google_copying_label.place(x=0, y=170)

        self.manual_google_upload_checkbox = tk.Checkbutton(self, variable=self.manual_google_upload_checkbox_state)
        self.manual_google_upload_checkbox.place(x=manual_google_copying_label.winfo_reqwidth(), y=170)
        self.manual_google_copy_guard(self.google_upload_checkbox_state.get())

        self.gdrive_target_folder_id = tk.Entry(self, width=43)
        if settings_dict["Google Folder ID"]:
            self.gdrive_target_folder_id.insert(0, settings_dict["Google Folder ID"])
        else:
            self.gdrive_target_folder_id.insert(0, "Google drive target folder ID")
            self.gdrive_target_folder_id.config(fg="grey")
        self.gdrive_target_folder_id.bind("<FocusIn>", lambda event: self.gdrive_focus_in(self.gdrive_target_folder_id))
        self.gdrive_target_folder_id.bind("<FocusOut>", lambda event: self.gdrive_focus_out(self.gdrive_target_folder_id))
        self.gdrive_target_folder_id.place(x=155, y=203)

    @staticmethod
    def revert_settings():
        values = {"Stickied Source": [""], "Stickied Destinations": ["", "", "", ""], "Auto Copy": [-1, False],
                  "Auto Delete": [-1, False], "Auto Close": [-1, False], "Last Auto Copy": False,
                  "Google Upload": False, "Manual Copy Upload": False, "Google Folder ID": False}
        loaded_settings.settings["Sources History"] = []
        loaded_settings.settings["Destinations History"] = []
        for setting in values.keys():
            loaded_settings.settings["Settings"][setting] = values[setting]
        loaded_settings.save_json()
        print("Settings erased. Press \"Save\" button if you wish to revert back.")

    def save_button(self):
        auto_copy_state = self.auto_copy_checkbox_state.get()
        auto_delete_state = self.auto_delete_checkbox_state.get()
        auto_close_state = self.auto_close_checkbox_state.get()
        google_upload_state = self.google_upload_checkbox_state.get()
        google_manual_upload_state = self.manual_google_upload_checkbox_state.get()
        copy_frequency = self.copy_frequency_entry.get()
        delete_frequency = self.delete_frequency_entry.get()
        seconds_until_close = self.seconds_until_close.get()
        gdrive_target_folder_id = self.gdrive_target_folder_id.get()

        settings_dict = loaded_settings.settings["Settings"]
        # Auto Copy CheckButton
        if auto_copy_state == 1:
            settings_dict["Auto Copy"][1] = True
        else:
            settings_dict["Auto Copy"][1] = False

        # Auto Delete CheckButton
        if auto_delete_state == 1:
            settings_dict["Auto Delete"][1] = True
        else:
            settings_dict["Auto Delete"][1] = False

        # Auto Close Checkbutton
        if auto_close_state == 1:
            settings_dict["Auto Close"][1] = True
        else:
            settings_dict["Auto Copy"][1] = False

        # Auto Copy Frequency
        if copy_frequency == "":
            settings_dict["Auto Copy"][0] = -1
        else:
            settings_dict["Auto Copy"][0] = copy_frequency

        # Auto Delete Frequency
        if delete_frequency == "":
            settings_dict["Auto Delete"][0] = -1
        else:
            settings_dict["Auto Delete"][0] = delete_frequency

        # Seconds Until Close
        if seconds_until_close == "":
            settings_dict["Auto Close"][0] = -1
        else:
            settings_dict["Auto Close"][0] = seconds_until_close

        # Google Upload
        if google_upload_state == 1:
            settings_dict["Google Upload"] = True
        else:
            settings_dict["Google Upload"] = False
        if google_manual_upload_state == 1:
            settings_dict["Manual Copy Upload"] = True
        else:
            settings_dict["Manual Copy Upload"] = False
        if gdrive_target_folder_id != "Google drive target folder ID":
            settings_dict["Google Folder ID"] = gdrive_target_folder_id
        else:
            settings_dict["Google Folder ID"] = False
        loaded_settings.save_json()

    def manual_google_copy_guard(self, checkbox_state):
        if checkbox_state == 0:
            self.manual_google_upload_checkbox_state = tk.IntVar(value=0)
            self.manual_google_upload_checkbox.configure(state="disabled", variable=self.manual_google_upload_checkbox_state)
        elif checkbox_state == 1:
            self.manual_google_upload_checkbox.configure(state="normal")

    @staticmethod
    def check_valid(P):
        if not P:
            return True
        try:
            int(P)
            return True
        except ValueError:
            return False

    @staticmethod
    def gdrive_focus_in(caller):
        if caller.get() == "Google drive target folder ID":
            caller.delete(0, "end")
            caller.insert(0, "")
            caller.config(fg="black")

    @staticmethod
    def gdrive_focus_out(caller):
        if caller.get() == "":
            caller.insert(0, "Google drive target folder ID")
            caller.config(fg="grey")

# TODO: Add a progress bar for copying


def main():
    app = GUI()
    app.title("File Auto Backup")
    app.geometry("710x260")
    app.mainloop()


if __name__ == "__main__":
    main()
