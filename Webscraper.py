#!./.env/bin/python3
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver import FirefoxProfile
# from selenium.webdriver import PhantomJS
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from selenium.webdriver.common.keys import Keys
import os
from abc import ABC

class SeleniumAddons(ABC):

    def wait_until_css_element_object_found(self, css_param, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, css_param)))

    def scroll_down_one_page(self, lines_down):
        self.browser.execute_script(
            "window.scrollTo(0, " + str(lines_down) + ")")

    def drag_and_drop(self, source_element_object, destination_element_object):
        ActionChains(self.browser).drag_and_drop(
            source_element_object, destination_element_object).perform()

    def hover_over(self, element_object):
        ActionChains(self.browser).move_to_element(element_object).perform()

    def is_present(self, element_object):
        try:
            # browser.find_element_by_css_selector("div")
            if element_object.is_displayed():
                return True
        except:
            return False

    def update_browser(self):
        for handle in self.browser.window_handles:
            self.browser.switch_to.window(handle)

    def wait_until_name_element_object_found(self, name_param, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located((By.NAME, name_param)))

    def wait_until_partial_link_text_element_object_found(self, partial_link_text, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, partial_link_text)))

    def wait_until_class_name_element_object_found(self, class_name, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, class_name)))

    def wait_until_id_element_object_found(self, id_object, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located((By.ID, id_object)))

    def wait_until_partial_link_text_object_found(self, id_object, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, id_object)))

    def multi_select_in_list(self, element_objects, labels):
        for option in element_objects:
            if option.text in labels:
                option.click()

    def select_in_list(self, element_objects, labels):
        for option in element_objects:
            if option.text in labels:
                option.click()
                break

class CustomChrome(SeleniumAddons):

    def __init__(self, incognito=True, headless=False, brave=False) -> None:
        options = ChromeOptions()

        # https://stackoverflow.com/questions/64927909/failed-to-read-descriptor-from-node-connection-a-device-attached-to-the-system
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        options.add_argument("disable-extensions")
        if incognito:
            options.add_argument("incognito")
        if headless:
            options.add_argument("headless")

        # options.add_argument("disable-gpu")
        # options.add_argument('window-size=1200x1200')
        # options.add_argument("remote-debugging-port=9222")
        # options.add_argument("kiosk")

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

class CustomFirefox(SeleniumAddons):

    def __init__(self, geckodriver_path=None, incognito=True, headless=False, service_log_path=None) -> None:
        super().__init__()
        options = FirefoxOptions()
        if incognito:
            options.add_argument("--incognito")
        if headless:
            options.add_argument("--headless")

        if os.name == 'nt':
            if geckodriver_path is None:
                geckodriver_path = str(Path('./FirefoxDrivers/Windows/geckodriver.exe').absolute())
            if service_log_path is None:
                service_log_path = str(Path('./FirefoxDrivers/Windows/gecko.log').absolute())
        elif os.name == 'posix':
            raise ValueError
        else:
            raise ValueError
        self.browser = Firefox(executable_path=geckodriver_path, options=options, service_log_path=service_log_path)

if __name__ == '__main__':
    browser_instance = CustomFirefox(incognito=True)
    browser_instance.browser.get('https://www.google.com')
    browser_instance.wait_until_name_element_object_found('q')
    elem = browser_instance.browser.find_element_by_name('q')
    elem.send_keys('hello')
    elem.send_keys(Keys.RETURN)

