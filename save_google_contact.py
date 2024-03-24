from pprint import pprint

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes for the Google Contacts API
SCOPES = ['https://www.googleapis.com/auth/contacts']


class SaveGoogleContact:

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
        print("Contact Groups:", results)
        for group in results.get('contactGroups', []):
            print("Group:", group)
            if group['name'] in labels:
                print("Label Found:", group['name'])
                label_ids.append(group['resourceName'])
        print("Label IDs:", label_ids)
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
            if "organizations" not in new_contact:
                new_contact["organizations"] = [{}]
            new_contact["organizations"][0]["title"] = job_title
        if website:
            new_contact["urls"] = [{"value": website}]
        if labels:
            label_ids = self.get_label_ids(labels)
            label_memberships = [{"contactGroupMembership": {"contactGroupResourceName": label_id}} for label_id in
                                 label_ids if label_id]
            new_contact["memberships"] = label_memberships

        # Create the contact
        created_contact = self.service.people().createContact(body=new_contact).execute()

        print("Contact created successfully:")
        pprint(created_contact)


if __name__ == '__main__':
    first_name = "Mr. Asikul Alam"
    last_name = "Khan"
    phone_number = "01757110099"
    email = "ceo@splendorit.com"
    company = "Splendor IT"
    job_title = "CEO"
    website = "www.priyoshop.com"
    labels = ["BASIS", "basis"]  # Example labels
    SaveGoogleContact().create_contact(first_name, last_name, phone_number, email, company,
                                       job_title, website, labels)
