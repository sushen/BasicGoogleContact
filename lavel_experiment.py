from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json

# Define the scopes for the Google Contacts API
SCOPES = ['https://www.googleapis.com/auth/contacts']


class SaveGoogleContact():

    def __init__(self):
        self.service = self.build_service()

    def build_service(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        return build('people', 'v1', credentials=creds)

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
            ],
            'memberships': []
        }

        # Add optional fields if provided
        if company or job_title:
            new_contact["organizations"] = [{"name": company, "title": job_title}]
        if website:
            new_contact["urls"] = [{"value": website}]

        # Add labels to memberships
        if labels:
            for label in labels:
                new_contact['memberships'].append({
                    'contactGroupMembership': {
                        'contactGroupResourceName': f'contactGroups/{label}'
                    }
                })

        # Print out the request body
        print("Request Body:")
        print(json.dumps(new_contact, indent=4))

        # Create the contact
        created_contact = self.service.people().createContact(body=new_contact).execute()

        print("Contact created successfully:")
        print(created_contact)


if __name__ == '__main__':
    first_name = "Mr. Yeaser"
    last_name = "Arafat"
    phone_number = "01814652640"
    email = "arafat@live-technologies.net"
    company = "Live Media Ltd."
    job_title = "Managing Director"
    website = "live-mediabd.net"
    SaveGoogleContact().create_contact(first_name, last_name, phone_number, email, company,
                                       job_title, website, labels=["BASIS"])
