import time
import re
from selenium.webdriver.common.by import By
from driver.driver import Driver
from save_google_contact import SaveGoogleContact


driver = Driver().driver
website_url = "https://basis.org.bd/member-list"
driver.get(website_url)
driver.implicitly_wait(10)
time.sleep(1)

input("Stop..:")

contact_x_path = "//div[@class='card-body pt-0']"
contact_elements = driver.find_element(By.XPATH, contact_x_path)
contact_text = contact_elements.text


def first_name_and_last_name(text):
    start_index = text.find("Representative") + len("Representative")
    end_index = text.find("Designation:")
    representative_info = text[start_index:end_index].strip()
    representative_lines = representative_info.split('\n')
    last_name = representative_lines[-1].split()[-1]
    first_name = representative_info[:-len(last_name)]
    # print("First Name:", first_name)
    # print("Last Name:", last_name)
    return first_name, last_name


# print(first_name_and_last_name(contact_text)[0])
# print(first_name_and_last_name(contact_text)[1])
# input("Name Work ..:")


def designation(text):
    start_index = text.find("Designation:") + len("Designation:")
    end_index = text.find("Contact:")
    designation = text[start_index:end_index].strip().split(":")[-1].strip()
    # print(designation)
    return designation


# print(designation(contact_text))
# input("Designation Work ..:")


def phone(text):
    start_index = text.find("Contact:") + len("Contact:")
    end_index = text.find("Email:")
    Contact = text[start_index:end_index].strip().split(":")[-1].strip()
    # print(Contact)
    return Contact


# print(phone(contact_text))


def email(text):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    emails_found = re.findall(email_pattern, text)
    email = emails_found[-1]
    # print(email)
    return email


# print(email(contact_text))

input("Phone and Email Work ..:")
# input("Stop ..:")

footer_address_xpath = "//div[@class='footer-address']"
footer_address_elements = driver.find_element(By.XPATH, footer_address_xpath)
footer_address_text = footer_address_elements.text


# print(footer_address_text)

def address(text):
    start_index = text.find("ADDRESS") + len("ADDRESS")
    # TODO: I have to work with Address
    end_index = text.find("Email:")
    ADDRESS = text[start_index:end_index].strip().split(":")[-1].strip()
    # print(ADDRESS)
    return ADDRESS


# print(address(footer_address_text))


def website(text):
    url_pattern = r"\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z]+)+)\b"
    matches = re.findall(url_pattern, text)
    web_address = matches[-1]
    # print(web_address)
    return web_address


# print(website(footer_address_text))


def company():
    company_details_xpath = "//div[@class='companyDetails']/h1"
    company_details_elements = driver.find_element(By.XPATH, company_details_xpath)
    company = company_details_elements.text
    # print(company)
    return company

# print(company())
# print("\n..........................")
input("Write To Google Contact ..:")


# job_title = designation
# phone_number = Contact
# phone_label = "Mobile"
# email = email
# email_label = "Work"
# company = company
# website = web_address
# labels = ["BASIS"]
SaveGoogleContact(). \
    create_contact(first_name=first_name_and_last_name(contact_text)[0],
                   last_name=first_name_and_last_name(contact_text)[1],
                   phone_number=phone(contact_text),
                   email=email(contact_text),
                   company=company(),
                   job_title=designation(contact_text),
                   website=website(footer_address_text),
                   labels=["BASIS"])
