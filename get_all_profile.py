"""
I Scrap 55 page, and I will start from there also.
"""

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


def save_profile_link():
    list_profile_xpath = "//div[@class='card card-body shadow-sm']//a[contains(.,'More Details')]"
    list_profile_elements = driver.find_elements(By.XPATH, list_profile_xpath)
    for element in list_profile_elements:
        # print(element.get_attribute("outerHTML"))
        html = element.get_attribute("outerHTML")

        pattern = r'href="(/company-profile/[^"]*)"'
        match = re.search(pattern, html)

        if match:
            url = match.group(1)
            url = f"https://basis.org.bd{url}"
            with open("extracted_url.txt", "r+") as file:
                urls = file.read()
                if url not in urls:
                    file.write(url + "\n")
                    print(f"{url}\nextracted and written to 'extracted_url.txt'.")
                else:
                    print("URL already exists in the file.")
        else:
            print("URL not found in the HTML.")
        # input("Stop..:")


while True:
    save_profile_link()
    input("Next Page..:")
