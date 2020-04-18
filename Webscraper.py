from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
import os


class LoginClass(object):

    def __init__(self, incognito=True, headless=False, brave=False):
        options = ChromeOptions()
        options.add_argument("disable-extensions")
        if incognito:
            options.add_argument("incognito")
        if headless:
            options.add_argument("headless")
        if os.name == 'nt':
            # path_to_chrome = str(Path('./chromedriver.exe').relative_to('.'))
            path_to_chrome = str(Path('./ChromeDrivers/Windows/chromedriver.exe').absolute())
        elif os.name == 'posix':
            path_to_chrome = str(Path('./ChromeDrivers/Mac/chromedriver').absolute())
        else:
            if brave:
                options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
            path_to_chrome = str(Path('./ChromeDrivers/Linux/chromedriver').absolute())
        self.browser = Chrome(path_to_chrome, options=options)

    def logging_in(self, url):
        self.browser.get(url)


if __name__ == '__main__':
    fetching_token = LoginClass()
    fetching_token.logging_in('https://www.google.com')
