import tkinter as tk
from tkinter import filedialog
from autoHandling import *
from fileWrite import *

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


class MainPage(tk.Frame, GUI):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Saved settings
        self.saved_settings_file = "AutoSettings.txt"

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
        copy_button = tk.Button(self, text="Copy!",
                                command=lambda: self.execute_copies(), padx=80, pady=2)
        copy_button.place(x=256, y=225)

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
        self.destination_path_entry1.insert(0, self.path_auto_insert_directory("destination_1"))
        self.destination_path_entry1.bind("<FocusIn>",
                                          lambda event: self.copy_selected_directory_to_bar(self.destination_path_entry1))
        self.destination_path_entry1.place(x=8, y=100, height=22, width=363)

        self.destination_path_entry2 = tk.Entry(self)
        self.destination_path_entry2.insert(0, self.path_auto_insert_directory("destination_2"))
        self.destination_path_entry2.bind("<FocusIn>",
                                          lambda event: self.copy_selected_directory_to_bar(self.destination_path_entry2))

        self.destination_path_entry2.place(x=8, y=130, height=22, width=363)

        self.destination_path_entry3 = tk.Entry(self)
        self.destination_path_entry3.insert(0, self.path_auto_insert_directory("destination_3"))
        self.destination_path_entry3.bind("<FocusIn>",
                                          lambda event: self.copy_selected_directory_to_bar(self.destination_path_entry3))
        self.destination_path_entry3.place(x=8, y=160, height=22, width=363)

        self.destination_path_entry4 = tk.Entry(self)
        self.destination_path_entry4.insert(0, self.path_auto_insert_directory("destination_4"))
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

        # Auto Run Check
        self.run_auto_check()

    def stick_directories(self):
        # Each entry bar is associated with a numerical key. The key is the line that will be written to for the
        # respective bar in AutoSettings.txt. Next time program is ran, the directories written will be inserted on start.
        bars = {15: self.source_path_entry.get(), 18: self.destination_path_entry1.get(),
                19: self.destination_path_entry2.get(), 20: self.destination_path_entry3.get(),
                21: self.destination_path_entry4.get()}
        lines = read_lines_from_file(self.saved_settings_file)
        for key in bars.keys():
            lines[int(key)] = f"{bars[key]}\n"
        write_lines_to_file(self.saved_settings_file, lines)

    def run_auto_check(self):
        auto_copy_execute(self.source_path_entry.get(), self.add_destination_directories_to_list(),
                          get_file_name(self.source_path_entry.get()))
        check_files_then_delete(self.add_destination_directories_to_list())

    def remove_directory_from_history(self, directory_passed):
        if (directory_passed == "Copy a file from a source for it to be in your history" or
                directory_passed == "Copy to a directory for it to be added to your history"):
            return
        if directory_passed in source_directories_list():
            remove_written_directory_from_file("Sources.txt", directory_passed)
            self.current_saved_removal_directory = ""
        elif directory_passed in destination_directories_list():
            remove_written_directory_from_file("Destinations.txt", directory_passed)
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
        bad_destination = False
        for directory in list_of_destination_directories:
            if not os.path.exists(directory):
                print(f"Destination directory \"{directory}\" does not exist.")
                bad_destination = True
        if bad_destination:
            return

        source_directory_file_write(source_directory)
        # Loops over every dictionary in the list and copies the source to each directory
        for i in list_of_destination_directories:
            copy_to_directory(source_directory, i, get_file_name(source_directory))
            destination_directory_file_write(i)

    def path_auto_insert_directory(self, caller):
        # Function will look in AutoSettings.txt and grab the value associated with the callers key.
        entries = {"source_1": 15, "destination_1": 18, "destination_2": 19,
                   "destination_3": 20, "destination_4": 21}
        lines = read_lines_from_file(self.saved_settings_file)
        return lines[entries[caller]].strip()

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

        # Back to main page
        back_home = tk.Button(self, text="Back",
                              command=lambda: controller.show_frame(MainPage), padx=10, pady=2)
        back_home.place(x=645, y=225)

        # Save settings
        save_settings = tk.Button(self, text="Save",
                                  command=lambda: self.save_button(), padx=10, pady=2)
        save_settings.place(x=585, y=225)

        # Erase settings
        erase_settings_button = tk.Button(self, text="Erase Settings", command=lambda: self.revert_settings(), padx=10,
                                          pady=2)
        erase_settings_button.place(x=475, y=225)

        # Saved Settings
        self.saved_settings_file = "AutoSettings.txt"
        lines = read_lines_from_file(self.saved_settings_file)

        # Auto Copy Checkbox State
        if lines[2].strip() == "YES":
            self.auto_copy_checkbox_state = tk.IntVar(value=1)
        else:
            self.auto_copy_checkbox_state = tk.IntVar(value=0)

        # Auto Delete Checkbox State
        if lines[6].strip() == "YES":
            self.auto_delete_checkbox_state = tk.IntVar(value=1)
        else:
            self.auto_delete_checkbox_state = tk.IntVar(value=0)

        # Auto Close Checkbox State
        if lines[9].strip() == "YES":
            self.auto_close_checkbox_state = tk.IntVar(value=1)
        else:
            self.auto_close_checkbox_state = tk.IntVar(value=0)

        # Auto copy
        auto_copy_label = tk.Label(self, text="Auto Copy?", font="LARGE_FONT")
        auto_copy_label.place(x=0, y=40)

        auto_copy_checkbox = tk.Checkbutton(self, variable=self.auto_copy_checkbox_state)
        auto_copy_checkbox.place(x=90, y=40)

        copy_frequency_label = tk.Label(self, text="Enter auto copy frequency (Days):", font="LARGE_FONT")
        copy_frequency_label.place(x=0, y=70)

        self.copy_frequency_entry = tk.Entry(self, width=3, font="LARGE_FONT")
        self.copy_frequency_entry.place(x=240, y=73)

        # Auto delete
        auto_delete_label = tk.Label(self, text="Auto Delete?", font="LARGE_FONT")
        auto_delete_label.place(x=500, y=40)

        auto_delete_checkbox = tk.Checkbutton(self, variable=self.auto_delete_checkbox_state)
        auto_delete_checkbox.place(x=600, y=40)

        delete_frequency_label = tk.Label(self, text="Delete after (Days):", font="LARGE_FONT")
        delete_frequency_label.place(x=500, y=70)

        self.delete_frequency_entry = tk.Entry(self, width=3, font="LARGE_FONT")
        self.delete_frequency_entry.place(x=642, y=73)

        # Auto Close
        auto_close_label = tk.Label(self, font="LARGE_FONT", text="Auto Close?")
        auto_close_label.place(x=500, y=120)
        auto_close = tk.Checkbutton(self, variable=self.auto_close_checkbox_state)
        auto_close.place(x=600, y=120)

        # Auto Copy Entry Set
        if lines[1].strip() == "-1":
            self.copy_frequency_entry.insert(0, "")
        else:
            self.copy_frequency_entry.insert(0, lines[1].strip())

        # Auto Delete Entry Set
        if lines[5].strip() == "-1":
            self.delete_frequency_entry.insert(0, "")
        else:
            self.delete_frequency_entry.insert(0, lines[5].strip())

        # Dropbox upload
        dropbox_upload_label = tk.Label(self, text="Dropbox upload?", font="LARGE_FONT")
        dropbox_upload_label.place(x=0, y=130)

        dropbox_upload_checkbox = tk.Checkbutton(self)
        dropbox_upload_checkbox.place(x=125, y=130)

        dropbox_login_label = tk.Label(self, text="Enter Dropbox login:", font="LARGE_FONT")
        dropbox_login_label.place(x=0, y=160)

        self.dropbox_login_entry = tk.Entry(self, width=43)
        self.dropbox_login_entry.insert(0, "Separate username/email and password with \":\"")
        self.dropbox_login_entry.config(fg="grey")
        self.dropbox_login_entry.bind("<FocusIn>",
                                      lambda event: self.login_entry_click(self.dropbox_login_entry))
        self.dropbox_login_entry.bind("<FocusOut>",
                                      lambda event: self.login_focus_out(self.dropbox_login_entry))
        self.dropbox_login_entry.place(x=150, y=163)

        # Google upload
        google_upload_label = tk.Label(self, text="Google drive upload?", font="LARGE_FONT")
        google_upload_label.place(x=0, y=190)

        google_upload_checkbox = tk.Checkbutton(self)
        google_upload_checkbox.place(x=158, y=190)

        google_login_label = tk.Label(self, text="Enter Google Login:", font="LARGE_FONT")
        google_login_label.place(x=0, y=220)

        self.google_login_entry = tk.Entry(self, width=43)
        self.google_login_entry.insert(0, "Separate username/email and password with \":\"")
        self.google_login_entry.config(fg="grey")
        self.google_login_entry.bind("<FocusIn>", lambda event: self.login_entry_click(self.google_login_entry))
        self.google_login_entry.bind("<FocusOut>", lambda event: self.login_focus_out(self.google_login_entry))
        self.google_login_entry.place(x=150, y=223)

    def revert_settings(self):
        lines = read_lines_from_file(self.saved_settings_file)
        line_values = {1: "-1\n", 2: "NO\n", 5: "-1\n", 6: "NO\n", 9: "NO\n",
                       15: "\n", 18: "\n", 19: "\n", 20: "\n", 21: "\n"}
        for key in line_values.keys():
            lines[key] = line_values[key]
        write_lines_to_file(self.saved_settings_file, lines)

    def save_button(self):
        auto_copy_state = self.auto_copy_checkbox_state.get()
        auto_delete_state = self.auto_delete_checkbox_state.get()
        auto_close_state = self.auto_close_checkbox_state.get()
        copy_frequency = self.copy_frequency_entry.get()
        delete_frequency = self.delete_frequency_entry.get()

        lines = read_lines_from_file(self.saved_settings_file)

        # Auto Copy CheckButton
        if auto_copy_state == int(1):
            lines[2] = "YES\n"
        else:
            lines[2] = "NO\n"

        # Auto Delete CheckButton
        if auto_delete_state == int(1):
            lines[6] = "YES\n"
        else:
            lines[6] = "NO\n"

        # Auto Close Checkbutton
        if auto_close_state == int(1):
            lines[9] = "YES\n"

        else:
            lines[9] = "NO\n"

        # Auto Copy Frequency
        if copy_frequency == "":
            lines[1] = "-1\n"
        else:
            lines[1] = str(f"{copy_frequency}\n")

        # Auto Delete Frequency
        if delete_frequency == "":
            lines[5] = "-1\n"
        else:
            lines[5] = str(f"{delete_frequency}\n")
        write_lines_to_file(self.saved_settings_file, lines)

    @staticmethod
    def login_entry_click(caller):
        if caller.get() == "Separate username/email and password with \":\"":
            caller.delete(0, "end")
            caller.insert(0, "")
            caller.config(fg="black")

    @staticmethod
    def login_focus_out(caller):
        if caller.get() == "":
            caller.insert(0, "Separate username/email and password with \":\"")
            caller.config(fg="grey")

# TODO ONLINE UPLOADING USING DROPBOX AND GOOGLE DRIVE.
# TODO CHECKSUM TO MAKE SURE COPIED FILES ARE EXACT COPIES
# TODO NEW AUTO DELETE CHECKBOX. WHEN CHECKED, AUTO DELETE WILL GIVE A LIST OF FILES READY TO BE DELETED WITH NUMBERS THE USER CAN ENTER NOTHING TO PROCEED NORMALLY. OR ENTER NUMBERS WITH COMMAS SEPERATING THEM TO IGNORE THE FILE.
# TODO WHITELISTING FEATURE TO IGNORE FILES.


if __name__ == "__main__":
    app = GUI()
    app.title("File Auto Backup")
    app.geometry("710x260")
    app.mainloop()
