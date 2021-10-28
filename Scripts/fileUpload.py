import os.path
import os
from copyLogic import add_time_to_file_name
from datetime import datetime as dt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload


class MyDrive:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        """Shows basic usage of the Drive v3 API.
            Prints the names and ids of the first 10 files the user has access to.
            """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except google.auth.exceptions.RefreshError:
                    os.remove('token.json')
                    print("Credentials could not be refreshed.")
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

    @staticmethod
    def check_file_date(creation_time, deletion_time):
        # Will be used to determine if a file is older enough to be deleted.
        formatting = "%Y-%m-%dT%H:%M:%S.%fZ"
        date_obj = dt.strptime(creation_time, formatting)
        date_obj = date_obj.date()
        today = dt.today().date()
        timedelta = today.day - date_obj.day
        if timedelta >= deletion_time:
            return True
        return False

    def delete_old_folders(self, list_of_files):
        for file_id in list_of_files:
            try:
                self.service.files().delete(fileId=file_id).execute()
            except Exception as e:
                print(f"[ERROR] {e}")

    def check_for_old_folders(self, backup_folder_id, deletion_time):
        # Search for files in parent folder. If they're older than deletion date they will be removed.
        is_specific_backup_folder = True
        files_deleted = False
        response = self.service.files().list(q=f"'{backup_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'", fields="files(createdTime, name, id)").execute()
        files = [file for file in response.get("files", [])]
        old_files = []
        for file in files:
            if "꞉" not in file.get("name"):
                is_specific_backup_folder = False
                continue
            check_time_greater_than_date = self.check_file_date(file.get("createdTime"), deletion_time)
            if check_time_greater_than_date:
                print(f"File \"{file.get('name')}\" deleted.")
                old_files.append(file.get("id"))
                files_deleted = True
                continue
        self.delete_old_folders(old_files)
        if not is_specific_backup_folder:
            print("[WARNING] You're copying/deleting files from a folder that has other files besides backed up ones in it. Recommend that you create a folder specifically for backups.\n")
        if not files_deleted:
            print("No files in Google drive deleted.")

    def create_folder(self, name, parent_folder):
        new_name = add_time_to_file_name(name)
        folder_data = {
            "name": new_name,
            "parents": [parent_folder],
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder = self.service.files().create(body=folder_data,
                                             fields="id, name").execute()
        print(f"Created folder \"{folder.get('name')}\"")
        return folder.get("id")

    @staticmethod
    def gather_files(path):
        file_list = []
        for file in os.listdir(path):
            file_list.append(f"{path}/{file}")
        return file_list

    def upload_files_to_folder(self, files, parent_folder_name, grandparent_folder_id):
        parent_folder_id = self.create_folder(parent_folder_name, grandparent_folder_id)
        for file in files:
            media = MediaFileUpload(f"{file}")
            name = os.path.split(file)[-1]
            file_metadata = {
                "name": name,
                "parents": [parent_folder_id]
            }
            file = self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()


def upload_files_to_google(path, backup_folder_id):
    folder_name = os.path.split(path)[-1]
    drive = MyDrive()
    files = drive.gather_files(path)
    drive.upload_files_to_folder(files, folder_name, backup_folder_id)


def delete_old_gdrive_backups(backup_folder_id, deletion_time):
    drive = MyDrive()
    drive.check_for_old_folders(backup_folder_id, deletion_time)


if __name__ == '__main__':
    files_path = input("Enter path to files: ")
    g_folder = input("Enter google folder id: ")
    upload_files_to_google(files_path, folder)
