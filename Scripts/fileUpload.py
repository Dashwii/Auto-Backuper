import os.path
import os
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
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

    @staticmethod
    def check_file_date(creation_time):
        # Will be used to determine if a file is older enough to be deleted.
        formatting = "%Y-%m-%dT%H:%M:%S.%fZ"
        date_obj = dt.strptime(creation_time, formatting)
        today = dt.today()
        timedelta = today - date_obj
        if timedelta.days >= 1:
            return True
        return False

    def check_for_old_folders(self, parent_folder):
        # Search for files in parent folder. If they're older than deletion date they will be removed.
        response = self.service.files().list(q=f"parents='{parent_folder}' and mimeType='application/vnd.google-apps.folder'", fields="files(createdTime, name)").execute()
        files = [file for file in response.get("files", [])]
        for file in files:
            check_time_greater_than_date = self.check_file_date(file.get("createdTime"))
            if check_time_greater_than_date:
                print(f"{file.get('name')} in Google drive will be deleted.")
                continue
            print(file.get("name"))

    def create_folder(self, name, parent_folder):
        folder_data = {
            "name": name,
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


if __name__ == '__main__':
    files_path = input("Enter path to files: ")
    g_folder = input("Enter google folder id: ")
    upload_files_to_google(files_path, folder)
