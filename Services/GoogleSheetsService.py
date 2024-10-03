import os.path
import re
import requests
import googleapiclient.discovery
import xlsxwriter
import Services.BrowserService
from Utils.ParserUtils import remove_extra_spaces
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from googleapiclient.http import *
from googleapiclient.discovery import *

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
secret_token = os.environ["SHEETS_TOKEN"]
apiKey = os.environ["SHEETS_API_KEY"]

def get_creds():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                secret_token, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def upload(workbook=xlsxwriter.Workbook):
    creds = get_creds()

    try:
        service = build("drive", "v3", credentials=creds)
        matches = re.findall(r'ExpensesFrom.+', workbook.filename)

        file_metadata = {"name": matches[0]}
        media = MediaFileUpload(workbook.filename, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        # pylint: disable=maybe-no-member
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        print(f'File ID: {file.get("id")}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None
    BrowserService.open_browser("https://docs.google.com/spreadsheets/d/{fileID}".format( fileID=file.get("id") ))
