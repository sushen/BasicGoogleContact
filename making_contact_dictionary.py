import json
import os
import re
import time

from selenium.webdriver.common.by import By
from driver.driver import Driver


def first_name_and_last_name(text):
    time.sleep(1)
    start_index = text.find("Representative") + len("Representative")
    end_index = text.find("Designation:")
    representative_info = text[start_index:end_index].strip()
    representative_lines = representative_info.split('\n')
    last_name = representative_lines[-1].split()[-1]
    first_name = representative_info[:-len(last_name)]
    return first_name.strip(), last_name.strip()


def designation(text):
    start_index = text.find("Designation:") + len("Designation:")
    end_index = text.find("Contact:")
    designation = text[start_index:end_index].strip().split(":")[-1].strip()
    return designation


def phone(text):
    start_index = text.find("Contact:") + len("Contact:")
    end_index = text.find("Email:")
    contact = text[start_index:end_index].strip().split(":")[-1].strip()
    return contact


def email(text):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    emails_found = re.findall(email_pattern, text)
    email = emails_found[-1]
    return email


def website(text):
    url_pattern = r"\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z]+)+)\b"
    matches = re.findall(url_pattern, text)
    web_address = matches[-1]
    return web_address


def company(xpath="//div[@class='companyDetails']/h1"):
    company_details_elements = driver.find_element(By.XPATH, xpath)
    company = company_details_elements.text
    return company


driver = Driver().driver

# Read processed URLs from done_collect_data.txt to avoid duplicates
processed_urls = set()
with open("done_collect_data.txt", "r") as done_file:
    for line in done_file:
        processed_urls.add(line.strip())

# Process URLs from extracted_url.txt if not already processed
with open("extracted_url.txt", "r") as input_file, open("done_collect_data.txt", "a") as output_file:
    for index, line in enumerate(input_file, start=1):
        line = line.strip()
        if line in processed_urls:
            print(f"Skipping line {index} as it is already processed.")
            continue

        print(f"{index}. {line}")

        driver.get(line)

        contact_x_path = "//div[@class='card-body pt-0']"
        contact_elements = driver.find_element(By.XPATH, contact_x_path)
        contact_text = contact_elements.text

        footer_address_xpath = "//div[@class='footer-address']"
        footer_address_elements = driver.find_element(By.XPATH, footer_address_xpath)
        footer_address_text = footer_address_elements.text

        contact_info = {
            "first_name": first_name_and_last_name(contact_text)[0],
            "last_name": first_name_and_last_name(contact_text)[1],
            "phone_number": phone(contact_text),
            "email": email(contact_text),
            "company": company(),
            "job_title": designation(contact_text),
            "website": website(footer_address_text),
            "labels": ["BASIS"]
        }

        # Load existing data from JSON file if available, or initialize as empty list
        data = []

        if os.path.exists("contact_info.json") and os.path.getsize("contact_info.json") > 0:
            try:
                with open("contact_info.json", "r") as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                print("Error loading JSON file. Initializing data as empty list.")

        # Check if contact_info already exists in data
        if contact_info not in data:
            # Append contact_info to data
            data.append(contact_info)

            # Save updated data to JSON file
            with open("contact_info.json", "w") as file:
                json.dump(data, file)

        # Write the processed URL into done_collect_data.txt
        output_file.write(line + "\n")

        # input("Stop:")

# Now you have the data in the 'data' list and it's also saved to the JSON file.
