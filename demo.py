import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# This defines the level of access you are requesting. For reading mail, this is sufficient.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
    """
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels and fetches a specific email.
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
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Build the Gmail API service
        service = build("gmail", "v1", credentials=creds)

        # --- Search for financial emails ---
        # You can customize the query. Examples:
        # 'from:yourbank@email.com subject:"Your monthly statement"'
        # 'subject:"transaction alert"'
        query = 'subject:"Your e-statement is ready"'
        
        # Call the Gmail API to search for messages
        result = service.users().messages().list(userId="me", q=query).execute()
        messages = result.get("messages", [])

        if not messages:
            print(f"No emails found matching the query: '{query}'")
            return
        
        print(f"Found {len(messages)} matching emails. Fetching the most recent one.")

        # Get the most recent email from the search results
        message_id = messages[0]["id"]
        # 'format': 'full' gets the entire email content, including headers and body
        msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()

        # --- Decode the Email Body ---
        payload = msg['payload']
        parts = payload.get('parts')

        data = ""
        if parts:
            # Emails can be multipart (e.g., plain text and HTML version)
            # We will look for the plain text part
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    break
        else:
            # If not multipart, the body is directly in the payload
            data = payload['body']['data']

        if data:
            # The email body is base64url encoded, so we need to decode it
            text = base64.urlsafe_b64decode(data).decode("utf-8")
            print("\n--- Email Content ---\n")
            print(text)
        else:
            print("\nCould not find plain text content in the email.")


    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()