import typing as typ

import googleapiclient.discovery as gdsc
from googleapiclient.errors import HttpError
import googleapiclient.http as ghttp

import src.CONFIG as CFG
import src.GmailApiInteraction.Credentials.GmailCredentialManager as gcm


class GmailController:

    def __init__(self):
        try:
            creds = gcm.GmailCredentialManager.getCredentials()
            service: gdsc.Resource = gdsc.build("gmail",
                                                "v1",
                                                credentials=creds)
            self._users_resource: gdsc.Resource = service.users()
            print(self._users_resource)
        except HttpError as error:
            print(f"An error occured: {error}")

    def _get_message_ids(self,
                         q: str) -> typ.List[typ.Dict[str, str]]:
        """

        Args:
            q: gmail query.

        Returns: messages ids corresponding to query

        """
        try:
            http_response = self._users_resource.messages().list(userId="me",
                                                                 q=q).execute()
            return http_response["messages"]

        except HttpError as error:
            print(f"An error occured: {error}")

    def get_raw_messages(self,
                         q: str = CFG.SEARCH_STRING_LIDER) -> typ.List[ghttp.HttpRequest]:
        try:
            return [self._users_resource.messages().get(userId="me",
                                                        id=ident["id"])
                    for ident in self._get_message_ids(q=q)]
        except HttpError as error:
            print(f"An error occured: {error}")

    def get_labels(self) -> None:
        """
        Shows basic usage of the Gmail API . Lists user's Gmail labels.

        Returns:

        """

        try:

            results = self._users_resource.labels().list(userId="me").execute()
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
    gc = GmailController()
    print(gc.get_raw_messages())
