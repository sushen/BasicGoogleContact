import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pathlib
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from save_google_contact import SaveGoogleContact


# chrome_options = Options()

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("debuggerAddress", "localhost:8797")
scriptDirectory = pathlib.Path().absolute()
# scriptDirectory = pathlib.PurePath("../driver")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-web-security")
# chrome_options.add_argument("--headless")

chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# chrome_options.add_argument("--user-data-dir=chrome-data")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument('--profile-directory=Profile 8')
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('disable-infobars')
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("user-data-dir=chrome-data")
# TODO: We have to solve the userdata problem it have to in one directory
chrome_options.add_argument(f"user-data-dir={scriptDirectory}\\userdata")

service = Service(executable_path="C:\\Users\\user\\PycharmProjects\\BasicGoogleContact\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)


driver.get("https://basis.org.bd/company-profile/13-08-523")
driver.implicitly_wait(10)
time.sleep(1)

contact_x_path = "//div[@class='card-body pt-0']"
contact_elements = driver.find_element(By.XPATH, contact_x_path)
contact_text = contact_elements.text
# print(contact_text)

# print("\n..........................")

start_index = contact_text.find("Representative") + len("Representative")
end_index = contact_text.find("Designation:")
representative_info = contact_text[start_index:end_index].strip()
representative_lines = representative_info.split('\n')
last_name = representative_lines[-1].split()[-1]
first_name = representative_info[:-len(last_name)]

print("First Name:", first_name)
print("Last Name:", last_name)

# Find the start and end indices of the relevant substring
start_index = contact_text.find("Designation:") + len("Designation:")
end_index = contact_text.find("Contact:")
designation = contact_text[start_index:end_index].strip().split(":")[-1].strip()
print(designation)

# Find the start and end indices of the relevant substring
start_index = contact_text.find("Contact:") + len("Contact:")
end_index = contact_text.find("Email:")
Contact = contact_text[start_index:end_index].strip().split(":")[-1].strip()
print(Contact)


email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
emails_found = re.findall(email_pattern, contact_text)
email = emails_found[-1]
print(email)

# input("Stop ..:")

footer_address_xpath = "//div[@class='footer-address']"
footer_address_elements = driver.find_element(By.XPATH, footer_address_xpath)
footer_address_text = footer_address_elements.text
# print(footer_address_text)

# TODO: I have to work with Address
start_index = footer_address_text.find("ADDRESS") + len("ADDRESS")
end_index = footer_address_text.find("Email:")
ADDRESS = footer_address_text[start_index:end_index].strip().split(":")[-1].strip()
print(ADDRESS)

url_pattern = r"\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z]+)+)\b"
matches = re.findall(url_pattern, footer_address_text)
web_address = matches[-1]
print(web_address)

company_details_xpath = "//div[@class='companyDetails']/h1"
company_details_elements = driver.find_element(By.XPATH, company_details_xpath)
company = company_details_elements.text
print(company)

print("\n..........................")
# input("Find Company Stop ..:")

last_name = last_name
first_name = first_name
job_title = designation
phone_number = Contact
phone_label = "Mobile"
email = email
email_label = "Work"
company = company
website = web_address
# TODO: Find A way to create Level
contact_group_id = "label/6715d2620c768d38"
SaveGoogleContact()\
    .create_contact(first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    phone_label=phone_label,
                    email=email,
                    email_label=email_label,
                    contact_group_id=contact_group_id,
                    company=company,
                    job_title=job_title,
                    website=website)

input("Stop ..:")
