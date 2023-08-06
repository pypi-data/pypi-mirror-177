
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path

# source: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens

# ===
# The following steps show how your application interacts with Google's OAuth 2.0 server to obtain 
# a user's consent to perform an API request on the user's behalf. 
# Your application must have that consent before it can execute a Google API request that 
# requires user authorization.
#
# The list below quickly summarizes these steps:
# 
# 1. Your application identifies the permissions it needs.
# 2. Your application redirects the user to Google along with the list of requested permissions.
# 3. The user decides whether to grant the permissions to your application.
# 4. Your application finds out what the user decided.
# 5. If the user granted the requested permissions, your application retrieves tokens needed to make 
#    API requests on the user's behalf.
# ===

# source: https://developers.google.com/identity/protocols/oauth2/scopes#sheets
# See, edit, create and delete
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] 

class Auth:
    """
    The Class `Auth` will authenticate the current user with Google's account
    """

    def get(self) -> object:
        # adding here the oauth part

        # -TODO: [???] Implement code to read the credentials json file from Secret Manager
        # -TODO: [???] Add a handler to work with AWS Secret Manager (to store the token.json) ...
        # -TODO: encrypt the 'token.json' content in the memory 

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        creds = None

        (os.chdir(path=str(Path.home()) + '/crgoauth'))

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

        return creds