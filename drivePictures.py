from datetime import date
import random
from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

SERVICE_ACCOUNT_FILE = './service-account-key.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=credentials)

def list_files(folder_id) -> List[any]:
    """List all files in a specified Google Drive folder."""
    query = f"'{folder_id}' in parents and mimeType contains 'image/'"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name)", pageSize=1000).execute()
    items = results.get('files', [])    
    return items

def download_file(file_id, file_name, base_path):
    """Download a file from Google Drive."""
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(base_path + file_name, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        if status:
            print(f"Download {int(status.progress() * 100)}%.")
        else:
            print("Download complete!")

def download_random_image(base_path):
    try:
        with open("drive_folder_id") as folder_id_file:
            folder_id = folder_id_file.read().strip()
            image_files = list_files(folder_id)

            random.seed(date.today().isoformat())
            cur_image = random.choice(image_files)
            download_file(cur_image['id'], cur_image['name'], base_path)
            return cur_image['name']
    except Exception as e:
        print(f"Error with reading drive_folder_id file: {e}")