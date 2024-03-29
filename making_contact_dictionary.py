import json
import os
import re
import time
from selenium.webdriver.common.by import By
from driver.driver import Driver


class ContactProcessor:
    def __init__(self):
        self.driver = Driver().driver

    def first_name_and_last_name(self, text):
        start_index = text.find("Representative") + len("Representative")
        end_index = text.find("Designation:")
        representative_info = text[start_index:end_index].strip()
        representative_lines = representative_info.split('\n')
        last_name = representative_lines[-1].split()[-1]
        first_name = representative_info[:-len(last_name)]
        return first_name.strip(), last_name.strip()

    def designation(self, text):
        start_index = text.find("Designation:") + len("Designation:")
        end_index = text.find("Contact:")
        designation = text[start_index:end_index].strip().split(":")[-1].strip()
        return designation

    def phone(self, text):
        start_index = text.find("Contact:") + len("Contact:")
        end_index = text.find("Email:")
        contact = text[start_index:end_index].strip().split(":")[-1].strip()
        return contact

    def email(self, text):
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        emails_found = re.findall(email_pattern, text)
        email = emails_found[-1]
        return email

    def website(self, text):
        url_pattern = r"\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z]+)+)\b"
        matches = re.findall(url_pattern, text)
        if matches:
            web_address = matches[-1]
        else:
            web_address = ""
        return web_address

    def company(self, xpath="//div[@class='companyDetails']/h1"):
        company_details_elements = self.driver.find_element(By.XPATH, xpath)
        company = company_details_elements.text
        return company

    def process_contacts(self):
        processed_urls = set()

        with open("done_collect_data.txt", "r") as done_file:
            for line in done_file:
                processed_urls.add(line.strip())

        with open("extracted_url.txt", "r") as input_file, open("done_collect_data.txt", "a") as output_file:
            for index, line in enumerate(input_file, start=1):
                line = line.strip()
                if line in processed_urls:
                    print(f"Skipping line {index} as it is already processed.")
                    continue

                print(f"{index}. {line}")

                self.driver.get(line)

                self.driver.implicitly_wait(10)
                time.sleep(1)

                contact_x_path = "//div[@class='card-body pt-0']"
                contact_elements = self.driver.find_element(By.XPATH, contact_x_path)
                contact_text = contact_elements.text

                footer_address_xpath = "//div[@class='footer-address']"
                footer_address_elements = self.driver.find_element(By.XPATH, footer_address_xpath)
                footer_address_text = footer_address_elements.text

                contact_info = {
                    "first_name": self.first_name_and_last_name(contact_text)[0],
                    "last_name": self.first_name_and_last_name(contact_text)[1],
                    "phone_number": self.phone(contact_text),
                    "email": self.email(contact_text),
                    "company": self.company(),
                    "job_title": self.designation(contact_text),
                    "website": self.website(footer_address_text),
                    "labels": ["BASIS"]
                }

                data = []

                if os.path.exists("contact_info.json") and os.path.getsize("contact_info.json") > 0:
                    try:
                        with open("contact_info.json", "r") as file:
                            data = json.load(file)
                    except json.JSONDecodeError:
                        print("Error loading JSON file. Initializing data as empty list.")

                if contact_info not in data:
                    data.append(contact_info)

                    with open("contact_info.json", "w") as file:
                        json.dump(data, file)

                output_file.write(line + "\n")
                # input("Next..:")


if __name__ == "__main__":
    processor = ContactProcessor()
    processor.process_contacts()
