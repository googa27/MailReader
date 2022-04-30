import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GmailController:
    _SCOPES: [str] = ['https://www.googleapis.com/auth/gmail.readonly']
    _PATH_CREDENTIALS: str = "credentials.json"
    _PATH_TOKEN: str = "token.json"

    @classmethod
    def _login(cls, creds):
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cls._PATH_CREDENTIALS,
                                                             cls._SCOPES)
            creds = flow.run_local_server(port=0)
        return creds

    @classmethod
    def _save_creds(cls, creds):
        with open(cls._PATH_TOKEN, "w") as token:
            token.write(creds.to_json())

    @classmethod
    def _manageCredentials(cls):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(cls._PATH_TOKEN):
            creds = Credentials.from_authorized_user_file(cls._PATH_TOKEN,
                                                          cls._SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            creds = cls._login(creds)
            # Save the credentials for the next run
            cls._save_creds(creds)
        return creds

    @classmethod
    def get_labels(cls) -> None:
        """
        SHOWS basic usage of the Gmail API . Lists user's Gmail labels.

        :return:
        """

        creds = cls._manageCredentials()

        try:
            # Call teh Gmail API
            service = build("gmail", "v1", credentials=creds)
            results = service.users().labels().list(userId="me").execute()
            labels = results.get("labels", [])

            if not labels:
                print("No labels found.")
                return
            print("Labels:")
            for label in labels:
                print(label["name"])
        except HttpError as error:
            print(f"Type of error thingy {type(error)}")
            print(f"An error occured: {error}")


if __name__ == '__main__':
    GmailController.get_labels()
