import time
import re

import pyautogui
from selenium.webdriver.common.by import By
from driver.driver import Driver
from save_google_contact import SaveGoogleContact


def first_name_and_last_name(text):
    start_index = text.find("Representative") + len("Representative")
    end_index = text.find("Designation:")
    representative_info = text[start_index:end_index].strip()
    representative_lines = representative_info.split('\n')
    last_name = representative_lines[-1].split()[-1]
    first_name = representative_info[:-len(last_name)]
    return first_name, last_name


def designation(text):
    start_index = text.find("Designation:") + len("Designation:")
    end_index = text.find("Contact:")
    designation = text[start_index:end_index].strip().split(":")[-1].strip()
    return designation


def phone(text):
    start_index = text.find("Contact:") + len("Contact:")
    end_index = text.find("Email:")
    Contact = text[start_index:end_index].strip().split(":")[-1].strip()
    print(Contact)
    return Contact


def email(text):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    emails_found = re.findall(email_pattern, text)
    email = emails_found[-1]
    return email





def address(text):
    start_index = text.find("ADDRESS") + len("ADDRESS")
    # TODO: I have to work with Address
    end_index = text.find("Email:")
    ADDRESS = text[start_index:end_index].strip().split(":")[-1].strip()
    return ADDRESS


def website(text):
    url_pattern = r"\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z]+)+)\b"
    matches = re.findall(url_pattern, text)
    web_address = matches[-1]
    return web_address


def company(xpath="//div[@class='companyDetails']/h1"):
    # company_details_xpath = "//div[@class='companyDetails']/h1"
    company_details_elements = driver.find_element(By.XPATH, xpath)
    company = company_details_elements.text
    return company


driver = Driver().driver
with open("extracted_url.txt", "r") as file:
    for index, line in enumerate(file):
        print(f"{index}. {line.strip()}")

        driver.get(line.strip())
        # input("Stop..:")

        contact_x_path = "//div[@class='card-body pt-0']"
        contact_elements = driver.find_element(By.XPATH, contact_x_path)
        contact_text = contact_elements.text

        footer_address_xpath = "//div[@class='footer-address']"
        footer_address_elements = driver.find_element(By.XPATH, footer_address_xpath)
        footer_address_text = footer_address_elements.text

        SaveGoogleContact(). \
            create_contact(first_name=first_name_and_last_name(contact_text)[0],
                           last_name=first_name_and_last_name(contact_text)[1],
                           phone_number=phone(contact_text),
                           email=email(contact_text),
                           company=company(),
                           job_title=designation(contact_text),
                           website=website(footer_address_text),
                           labels=["BASIS"])

        # input("Stop..:")
