from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://basis.org.bd/company-profile/03-09-017")
contact_x_path = "//div[@class='card-body pt-0']"
contact_elements = driver.find_element(By.XPATH, contact_x_path)
contact_text = contact_elements.text
print(contact_text)

print("\n..........................")

footer_address_xpath = "//div[@class='footer-address']"
footer_address_elements = driver.find_element(By.XPATH, footer_address_xpath)
footer_address_text = footer_address_elements.text
print(footer_address_text)

input("Stop ..:")
