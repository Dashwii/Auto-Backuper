import os
from fileWrite import loaded_settings
from copyLogic import add_time_to_file_name
from datetime import datetime as dt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

SCOPE = ["https://www.googleapis.com/auth/drive"]


def get_creds():
    flow = InstalledAppFlow.from_client_secrets_file("..\config\credentials.json", scopes=SCOPE)
    return flow.run_local_server(port=0)


def gather_files(path):
    file_list = []
    for file in os.listdir(path):
        file_list.append(f"{path}/{file}")
    return file_list


def authorize():
    creds = False
    token_path = r"..\config\token.json"
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPE)
    # If there are no (valid) credentials available, let user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"[ERROR] Credentials could not be refreshed. {e}")
                os.remove(token_path)
                creds = ask_if_user_wants_creds()
                if creds is None:
                    disable_uploading()
                    return
        else:
            print(f"[ERROR] Credentials could not be refreshed.")
            creds = ask_if_user_wants_creds()
            if creds is None:
                disable_uploading()
                return

        # Save credentials for future use
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    if creds:
        service = build("drive", "v3", credentials=creds)
        return service


def ask_if_user_wants_creds():
    response = input("Do you want to enable google drive uploading? Y/N\n")
    if response.lower() in ("yes", "y"):
        creds = get_creds()
        return creds
    elif response.lower() in ("no", "n"):
        return None


def create_folder(name, parent_folder, service):
    new_name = add_time_to_file_name(name)
    folder_data = {
        "name": new_name,
        "parents": [parent_folder],
        "mimeType": "application/vnd.google-apps.folder"
    }
    folder = service.files().create(body=folder_data, fields="id, name").execute()
    print(f"Created folder \"{folder.get('name')}\"")
    return folder.get("id")


def upload_files_to_folder(files, parent_folder_name, grandparent_folder_id, service):
    # Maybe turn into async function and yield the files finished? Might have to turn into class and add a variable for
    # files currently finished in the current upload
    parent_folder_id = create_folder(parent_folder_name, grandparent_folder_id, service)
    for file in files:
        media = MediaFileUpload(f"{file}")
        name = os.path.split(file)[-1]
        file_metadata = {
            "name": name,
            "parents": [parent_folder_id]
        }
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()


def upload_files_to_google(path, backup_folder_id):
    folder_name = os.path.split(path)[-1]
    drive = authorize()
    if drive is not None:
        files = gather_files(path)
        upload_files_to_folder(files, folder_name, backup_folder_id, drive)


def check_if_file_max_age(creation_time, max_age):
    formatting = "%Y-%m-%dT%H:%M:%S.%fZ"
    date_obj = dt.strptime(creation_time, formatting)
    date_obj = date_obj.date()
    today = dt.today().date()
    timedelta = today - date_obj
    timedelta = int(timedelta.days)
    if timedelta >= max_age:
        return True
    return False


def delete_old_folders(service, target_folder_id):
    for file_id in target_folder_id:
        try:
            service.files().delete(fileId=file_id).execute()
        except Exception as e:
            print("[ERROR]", e)


def check_for_old_folders(service, backup_folder_id, max_age):
    is_dedicated_backup_folder = True
    files_deleted = False
    try:
        response = service.files().list(q=f"'{backup_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'", fields="files(createdTime, name, id)").execute()
    except Exception as e:
        print("[ERROR]", e)
        return
    files = [file for file in response.get("files", [])]
    old_files = []
    for file in files:
        if "꞉" not in file.get("name"):  # If ꞉ not in the file name then skip the file and warn the user about dedicating a folder for backups.
            is_dedicated_backup_folder = False
            continue
        check_time_greater_than_date = check_if_file_max_age(file.get("createdTime"), max_age)
        if check_time_greater_than_date:
            print(f"File \"{file.get('name')} deleted.")
            old_files.append(file.get("id"))
            files_deleted = True
            continue
    delete_old_folders(service, old_files)
    if not is_dedicated_backup_folder:
        print("[WARNING] You're copying/deleting files from a folder that has other files besides backed up ones in it. Recommend that you create a folder specifically for backups.\n")
    if not files_deleted:
        print("No files in Google drive deleted.")


def delete_old_gdrive_backups(backup_folder_id, max_age):
    max_age = int(max_age)
    drive = authorize()
    if drive is not None:
        check_for_old_folders(drive, backup_folder_id, max_age)


def disable_uploading():
    loaded_settings.settings["Settings"]["Google Upload"] = False
    loaded_settings.save_json()
    print("Google uploading disabled")


if __name__ == '__main__':
    files_path = input("Enter path to files: ")
    g_folder = input("Enter google folder id: ")
    upload_files_to_google(files_path, g_folder)
