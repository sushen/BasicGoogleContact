from pprint import pprint
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the scopes for the Google Contacts API
SCOPES = ['https://www.googleapis.com/auth/contacts']


class SaveGoogleContact:

    def __init__(self):
        self.service = self.build_service()

    def build_service(self):
        # Load saved refresh token
        def load_refresh_token():
            try:
                with open("../refresh_token.txt", "r") as file:
                    return file.read().strip()
            except FileNotFoundError:
                print("Refresh token file not found.")
                return None

        refresh_token = load_refresh_token()
        if refresh_token is None:
            print("Refresh token is missing or invalid.")
            # Handle the error condition appropriately, such as exiting the program or prompting the user to provide the refresh token again.
            exit(1)

        # Use refresh token to obtain credentials
        def get_credentials():
            credentials = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id="1052058814383-2s503ud9diredv3117t5m2foq9i0cift.apps.googleusercontent.com", # Your client ID
                client_secret="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", # Your client secret
                scopes=SCOPES
            )
            return credentials

        # Obtain credentials
        credentials = get_credentials()

        # Refresh the credentials to obtain access token
        credentials.refresh(Request())

        # Build service with obtained access token
        service = build('people', 'v1', credentials=credentials)
        return service

    def get_label_ids(self, labels):
        # Fetch label IDs from Google Contacts API
        label_ids = []
        results = self.service.contactGroups().list().execute()
        for group in results.get('contactGroups', []):
            if group['name'] in labels:
                label_ids.append(group['resourceName'])
        return label_ids

    def create_contact(self, first_name, last_name, phone_number, email, company=None,
                       job_title=None, website=None, labels=None):
        # Define the contact you want to create
        new_contact = {
            "names": [
                {
                    "givenName": first_name,
                    "familyName": last_name
                }
            ],
            "phoneNumbers": [
                {
                    "value": phone_number,
                    "type": "mobile"
                }
            ],
            "emailAddresses": [
                {
                    "value": email,
                    "type": "work"
                }
            ]
        }

        # Add optional fields if provided
        if company:
            new_contact["organizations"] = [{"name": company}]
        if job_title:
            new_contact["organizations"][0]["title"] = job_title
        if website:
            new_contact["urls"] = [{"value": website}]
        if labels:
            label_ids = self.get_label_ids(labels)
            label_memberships = [{"contactGroupMembership": {"contactGroupId": label_id}} for label_id in label_ids if label_id]
            new_contact["memberships"] = label_memberships

        # Create the contact
        created_contact = self.service.people().createContact(body=new_contact).execute()

        print("Contact created successfully:")
        pprint(created_contact)


if __name__ == '__main__':
    first_name = "Mango"
    # first_name = input("First Name:")
    last_name = "Hulio"
    # last_name = input("Last Name:")
    phone_number = "=8801725588360"
    # phone_number = input("Phone Number:")
    email = "hjjdacnnj@gmail.com"
    # email = input("Email:")
    company = "Masdog"
    # company = input("Company:")
    job_title = "Sexy"
    # job_title = input("Job Title:")
    website = input("Website:")
    SaveGoogleContact().create_contact(first_name, last_name, phone_number, email, company,
                                       job_title, website, labels=["BASIS"])
