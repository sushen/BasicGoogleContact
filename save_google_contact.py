from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes for the Google Contacts API
SCOPES = ['https://www.googleapis.com/auth/contacts']

def create_contact(name, phone_number):
    # Set up the OAuth 2.0 flow for user authorization
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Build the Google Contacts API service
    service = build('people', 'v1', credentials=creds)

    # Define the contact you want to create
    new_contact = {
        "names": [
            {
                "givenName": name
            }
        ],
        "phoneNumbers": [
            {
                "value": phone_number
            }
        ]
    }

    # Create the contact
    created_contact = service.people().createContact(body=new_contact).execute()

    print("Contact created successfully:")
    print(created_contact)

if __name__ == '__main__':
    name = "Mr. Syed Almas Kabir"
    phone_number = "01711521964"
    create_contact(name, phone_number)
