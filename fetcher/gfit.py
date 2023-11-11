import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/fitness.heart_rate.read",
    "https://www.googleapis.com/auth/fitness.location.read",
]

CREDS = "fetcher/creds_bemyak.json"


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS, SCOPES)
            creds = flow.run_local_server(port=37585)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Print dataStreamId's

    # try:
    #     service = build("fitness", "v1", credentials=creds)
    #     response = service.users().dataSources().list(userId="me").execute()
    #     # print(json.dumps(response, sort_keys=True, indent=4))
    #     for r in response.values():
    #         for x in r:
    #             print(x["dataStreamId"])

    #     # Retrieve the documents contents from the Docs service.
    #     # document = service.documents().get(documentId=DOCUMENT_ID).execute()

    #     # print(f"The title of the document is: {document.get('title')}")
    # except HttpError as err:
    #     print(err)

    dataSourceId = "raw:com.google.distance.delta:com.google.android.apps.fitness:Xiaomi:Mi-4c:dd56c804:user_input"
    try:
        service = build("fitness", "v1", credentials=creds)
        response = (
            service.users()
            .dataSources()
            .datasets()
            .get(
                userId="me",
                datasetId=dataSourceId,
                datasetId=datetime.datetime.now().isoformat(),
            )
            .execute()
        )
        # print(json.dumps(response, sort_keys=True, indent=4))
        for r in response.values():
            for x in r:
                print(x["dataStreamId"])

        # Retrieve the documents contents from the Docs service.
        # document = service.documents().get(documentId=DOCUMENT_ID).execute()

        # print(f"The title of the document is: {document.get('title')}")
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
