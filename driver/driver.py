import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

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

class Driver:
    def __init__(self):
        self.driver = webdriver.Chrome(service=service, options=chrome_options)



# Driver().driver.get("https://www.google.com/")