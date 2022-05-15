import typing as typ
import pathlib as pth

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import src.CONFIG as CFG


class GmailCredentialManager:
    """
    In Charge of managing google API's credentials.
    """
    _SCOPES: typ.List[str] = CFG.SCOPES
    _PATH_CREDENTIALS: pth.Path = CFG.PATH_CREDENTIALS_DATA / "credentials.json"
    _PATH_TOKEN: pth.Path = CFG.PATH_CREDENTIALS_DATA / "token.json"

    @classmethod
    def _login(cls, creds) -> Credentials:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cls._PATH_CREDENTIALS,
                                                             cls._SCOPES)
            creds = flow.run_local_server(port=0)
        return creds

    @classmethod
    def _save_creds(cls, creds) -> None:
        with cls._PATH_TOKEN.open("w") as token:
            token.write(creds.to_json())

    @classmethod
    def getCredentials(cls) -> Credentials:
        creds = None
        if cls._PATH_TOKEN.is_file():
            creds = Credentials.from_authorized_user_file(cls._PATH_TOKEN,
                                                          cls._SCOPES)
        if not creds or not creds.valid:
            creds = cls._login(creds)
            cls._save_creds(creds)
        print(f"TYPE OF CREDS: {type(creds)}")
        return creds


if __name__ == '__main__':
    print(GmailCredentialManager.getCredentials())
