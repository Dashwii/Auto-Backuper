import tkinter as tk
from sys import exit
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
        frame.grid()


class MainPage(tk.Frame, GUI):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Clipboard saved directory
        self.source_saved_directory = ""
        self.destination_saved_directory = ""

        # Settings
        show_settings_button = tk.Button(self, text="Settings",
                                         command=lambda: controller.show_frame(SettingsPage), padx=10, pady=2)
        show_settings_button.place(x=628, y=225)

        # Copy
        copy_button = tk.Button(self, text="Copy!",
                                command=lambda: self.execute_copies(), padx=80, pady=2)
        copy_button.place(x=256, y=225)

        # Source Path Entry
        source_path_label = tk.Label(self, text="Source Path", fg="grey")
        source_path_label.place(x=6, y=5)

        self.source_path_entry = tk.Entry(self)
        self.source_path_entry.bind("<FocusIn>", lambda event: self.copy_to_source_bar(self.source_saved_directory))
        self.source_path_entry.insert(0, r"C:\Users\Dashw\AppData\Roaming\RenPy\Monika After Story")
        self.source_path_entry.place(x=8, y=25, height=22, width=363)

        # Source Browse Buttons
        source_path_browse = tk.Button(self, text="Browse", command=lambda: self.browse_paths(self.source_path_entry))
        source_path_browse.place(x=380, y=22)

        # Destination Path Entries
        self.destinations_paths_label = tk.Label(self, text="Destination Paths (Must have at least 1)", fg="grey")
        self.destinations_paths_label.place(x=6, y=78)

        self.destination_path_entry1 = tk.Entry(self)
        self.destination_path_entry1.insert(0, r"C:\Users\Dashw\Documents\Stuff\Games\DDLC\Monika Backups")
        self.destination_path_entry1.bind("<FocusIn>",
                                          lambda event: self.copy_to_destination_bar(self.destination_path_entry1,
                                                                                     self.destination_saved_directory))
        self.destination_path_entry1.place(x=8, y=100, height=22, width=363)

        self.destination_path_entry2 = tk.Entry(self)
        self.destination_path_entry2.insert(0, r"E:\MAS Backups")
        self.destination_path_entry2.bind("<FocusIn>",
                                          lambda event: self.copy_to_destination_bar(self.destination_path_entry2,
                                                                                     self.destination_saved_directory))
        self.destination_path_entry2.place(x=8, y=130, height=22, width=363)

        self.destination_path_entry3 = tk.Entry(self)
        self.destination_path_entry3.insert(0, r"F:\MAS Backups")
        self.destination_path_entry3.bind("<FocusIn>",
                                          lambda event: self.copy_to_destination_bar(self.destination_path_entry3,
                                                                                     self.destination_saved_directory))
        self.destination_path_entry3.place(x=8, y=160, height=22, width=363)

        self.destination_path_entry4 = tk.Entry(self)
        self.destination_path_entry4.bind("<FocusIn>",
                                          lambda event: self.copy_to_destination_bar(self.destination_path_entry4,
                                                                                     self.destination_saved_directory))
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

        source_directory_data = Sources.source_directories_list()
        self.source_variable_directory = tk.StringVar(controller)
        self.source_variable_directory.set("History")
        self.source_directory_history = tk.OptionMenu(self, self.source_variable_directory, *source_directory_data,
                                                      command=lambda x:
                                                      self.add_directory_clipboard(self.source_variable_directory))
        self.source_directory_history.place(x=430, y=18)


        # Destination History Button
        destination_directory_data = Destinations.destination_directories_list()
        self.destination_variable_directory = tk.StringVar(controller)
        self.destination_variable_directory.set("History")
        self.destination_directory_history = tk.OptionMenu(self, self.destination_variable_directory,
                                                           *destination_directory_data,
                                                           command=lambda x: self.add_directory_clipboard(
                                                               self.destination_variable_directory))
        self.destination_directory_history.place(x=430, y=93)

        # Auto Run Check
        self.auto_copy_check()
        self.auto_delete_check()



    def auto_copy_check(self):
        copy_instance = AutoCopy(self.source_path_entry.get(), get_file_name(self.source_path_entry.get()),
                                 *Destinations.destination_directories_list())
        copy_instance.auto_copy_execute()

    @staticmethod
    def auto_delete_check():
        delete_instance = AutoDelete().check_files_then_delete()

    def add_directory_clipboard(self, caller):
        if caller == self.source_variable_directory:
            self.source_saved_directory = self.source_variable_directory.get()
            self.source_variable_directory.set("History")
        else:
            self.destination_saved_directory = self.destination_variable_directory.get()
            self.destination_variable_directory.set("History")
        return

    def copy_to_source_bar(self, directory_passed):
        if directory_passed == self.destination_saved_directory:
            return
        else:
            if len(self.source_saved_directory) > 0:
                self.source_path_entry.delete(0, "end")
                self.source_path_entry.insert(0, self.source_saved_directory)
                return

    def copy_to_destination_bar(self, bar_name, directory):
        if directory == self.source_saved_directory:
            return
        if len(self.destination_saved_directory) > 0:
            bar_name.delete(0, "end")
            bar_name.insert(0, self.destination_saved_directory)
            self.destination_saved_directory = ""
        return

    def add_directories_to_list(self):
        """Adds directories from get() to a list then returns it"""
        list_of_directories = [self.destination_path_entry1.get(), self.destination_path_entry2.get(),
                               self.destination_path_entry3.get(), self.destination_path_entry4.get()]
        for i in list_of_directories[:]:
            if i == "":
                list_of_directories.remove(i)
        return list_of_directories

    def execute_copies(self):
        list_of_directories = self.add_directories_to_list()

        # Removes blank items from directory list
        for i in list_of_directories[:]:
            if i == "":
                list_of_directories.remove(i)

        if len(self.source_path_entry.get()) == 0:
            print("[ERROR] No source directory!")
            return
        if len(list_of_directories) == 0:
            print("[ERROR] No destinations given!")
            return

        Sources.source_directory_file_write(self.source_path_entry.get())
        # Loops over every dictionary in the list and copies the source to each directory
        for i in list_of_directories:
            print("")
            copy_to_directory(self.source_path_entry.get(), i, get_file_name(self.source_path_entry.get()))
            directory = Destinations(i)
            Destinations.destination_directory_file_write(directory)
        return

    @staticmethod
    def browse_paths(entry_box_path):
        source_path = filedialog.askdirectory()
        if len(source_path) == 0:
            return
        entry_box_path.delete(0, "end")
        entry_box_path.insert(0, source_path)


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

        # Set Checkbox States
        with open("Auto Settings.txt", "r") as file:
            lines = file.readlines()
            # Auto Copy Checkbox State
            if lines[2].strip() == "YES":
                self.auto_copy_checkbox_state = tk.IntVar(value=1)
            else:
                self.auto_copy_checkbox_state = tk.IntVar(value=0)

            # Auto Delete Checkbox State
            if lines[5].strip() == "YES":
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

        # Set Auto Entry States
        with open("Auto Settings.txt", "r") as file:
            lines = file.readlines()
            # Auto Copy Entry Set
            if lines[1].strip() == "-1":
                self.copy_frequency_entry.insert(0, "")
            else:
                self.copy_frequency_entry.insert(0, lines[1].strip())

            # Auto Delete Entry Set
            if lines[4].strip() == "-1":
                self.delete_frequency_entry.insert(0, "")
            else:
                self.delete_frequency_entry.insert(0, lines[4].strip())

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


    def save_button(self):
        auto_copy_state = self.auto_copy_checkbox_state.get()
        auto_delete_state = self.auto_delete_checkbox_state.get()
        auto_close_state = self.auto_close_checkbox_state.get()

        # Auto Copy CheckButton
        if auto_copy_state == int(1):
            with open("Auto Settings.txt", "r") as file:
                lines = file.readlines()
                lines[2] = "YES\n"
                with open("Auto Settings.txt", "w") as filewrite:
                    filewrite.writelines(lines)
        elif auto_copy_state == int(0):
            with open("Auto Settings.txt", "r") as file:
                lines = file.readlines()
                lines[2] = "NO\n"
                self.copy_frequency_entry.delete(0, "end")
                self.copy_frequency_entry.insert(0, "")
                with open("Auto Settings.txt", "w") as filewrite:
                    filewrite.writelines(lines)

        # Auto Delete CheckButton
        if auto_delete_state == int(1):
            with open("Auto Settings.txt", "r") as file:
                lines = file.readlines()
                lines[5] = "YES\n"
                with open("Auto Settings.txt", "w") as filewrite:
                    filewrite.writelines(lines)
        if auto_delete_state == int(0):
            with open("Auto Settings.txt", "r") as file:
                lines = file.readlines()
                lines[5] = "NO\n"
                self.delete_frequency_entry.delete(0, "end")
                self.delete_frequency_entry.insert(0, "")
                with open("Auto Settings.txt", "w") as filewrite:
                    filewrite.writelines(lines)

        # Auto Close Checkbutton
        with open("Auto Settings.txt", "r") as file:
            lines = file.readlines()
            with open("Auto Settings.txt", "w") as filewrite:
                if auto_close_state == int(1):
                    lines[9] = "YES\n"
                    filewrite.writelines(lines)
                else:
                    lines[9] = "NO\n"
                    filewrite.writelines(lines)

        # Auto Copy Frequency
        copy_frequency = self.copy_frequency_entry.get()
        with open("Auto Settings.txt", "r") as file:
            lines = file.readlines()
            if copy_frequency == "":
                lines[1] = "-1\n"
            else:
                lines[1] = str(f"{copy_frequency}\n")
            with open("Auto Settings.txt", "w") as filewrite:
                filewrite.writelines(lines)

        # Auto Delete Frequency
        delete_frequency = self.delete_frequency_entry.get()
        with open("Auto Settings.txt", "r") as file:
            lines = file.readlines()
            if delete_frequency == "":
                lines[4] = "-1\n"
            else:
                lines[4] = str(f"{delete_frequency}\n")
            with open("Auto Settings.txt", "w") as filewrite:
                filewrite.writelines(lines)

    def auto_close(self):
        state = self.auto_close_checkbox_state.get()
        print(state)

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


# TODO POP UP WINDOW DISPLAYING ALL FILES THAT WILL BE DELETED. YES/NO BUTTON AND SELECTION CHOICE FOR EACH FILE ON WHETHER THEY SHOULD BE DELETED.
# TODO ERROR MESSAGES POP UP IN GUI.
# TODO EASY REMOVAL OF DIRECTORIES FOR HISTORY.
# TODO ONLINE UPLOADING.
# TODO NEW AUTO DELETE CHECKBOX. WHEN CHECKED. AUTO DELETE WILL CHECK DIRECTORIES IN FILE. GATHER ALL FILES OLDER THAN DELETE DAY.
# TODO THEN IT WILL PROMPT USER FOR Y/N ON WHETHER FILES SHOULD BE DELETED. IF Y. FILES DELETED. IF N. FUNCTION RETURNS
# TODO CHANGE COPY LOGIC INTO CLASS
# TODO CHANGE AUTO DELETE INTO CLASS


if __name__ == "__main__":
    app = GUI()
    app.geometry("710x260")
    app.mainloop()
