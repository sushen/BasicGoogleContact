from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes for the Google Contacts API
SCOPES = ['https://www.googleapis.com/auth/contacts']


class SaveGoogleContact():

    def create_contact(first_name, last_name, phone_number, phone_label, email, email_label, contact_group_id=None,
                       company=None, job_title=None, website=None):
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
                    "givenName": first_name,
                    "familyName": last_name
                }
            ],
            "phoneNumbers": [
                {
                    "value": phone_number,
                    "type": phone_label
                }
            ],
            "emailAddresses": [
                {
                    "value": email,
                    "type": email_label
                }
            ]
        }

        # Add optional fields if provided
        if company:
            new_contact["organizations"] = [
                {
                    "name": company,
                    "type": "work"
                }
            ]
        if job_title:
            if "organizations" not in new_contact:
                new_contact["organizations"] = [{}]
            new_contact["organizations"][0]["title"] = job_title
        if website:
            new_contact["urls"] = [
                {
                    "value": website,
                    "type": "work"
                }
            ]

        # Add contact to specified contact group
        if contact_group_id:
            new_contact["memberships"] = [
                {
                    "contactGroupMembership": {
                        "contactGroupId": contact_group_id
                    }
                }
            ]

        # Create the contact
        created_contact = service.people().createContact(body=new_contact).execute()

        print("Contact created successfully:")
        print(created_contact)


if __name__ == '__main__':
    input("..:")
    first_name = "Mr. Asikul Alam"
    last_name = "Khan"
    phone_number = "01757110099"
    phone_label = "Mobile"
    email = "ceo@splendorit.com"
    email_label = "Work"
    company = "Splendor IT"
    job_title = "CEO"
    website = "www.priyoshop.com"
    contact_group_id = "label/6715d2620c768d38"  # Provide the ID of the contact group
    SaveGoogleContact().create_contact(first_name, last_name, phone_number, phone_label, email, email_label, contact_group_id, company,
                   job_title, website)
