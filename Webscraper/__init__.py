from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# TODO: Buildout FirefoxProfile
# from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from pathlib import Path
import os
from abc import ABC

class UnrecognizedOSError(NotImplementedError):
    pass

class ElementNotFound(Exception):
    pass

class SeleniumAddons(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.browser = WebDriver()

    def wait_until_css_element_object_found(self, css_param, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, css_param)))

    def scroll_down_x_lines(self, lines_down):
        self.browser.execute_script(
            "window.scrollTo(0, " + str(lines_down) + ")")

    def drag_and_drop(self, source_element_object, destination_element_object):
        ActionChains(self.browser).drag_and_drop(
            source_element_object, destination_element_object).perform()

    def hover_over(self, element_object):
        ActionChains(self.browser).move_to_element(element_object).perform()

    def is_present(self, element_object):
        try:
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
    
    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        print('Closing browser instance')
        self.browser.quit()

class CustomChrome(SeleniumAddons):

    def __init__(self, incognito=True, path_to_chrome=None, headless=False, disable_gpu=False, window_size=False) -> None:
        options = ChromeOptions()

        # https://stackoverflow.com/questions/64927909/failed-to-read-descriptor-from-node-connection-a-device-attached-to-the-system
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        options.add_argument("disable-extensions")
        if incognito:
            options.add_argument("incognito")
        if headless:
            options.add_argument("headless")
        if disable_gpu:
            options.add_argument("disable-gpu")
        if window_size:
            options.add_argument('window-size=1200x1200')
        # options.add_argument("remote-debugging-port=9222")
        # options.add_argument("kiosk")

        if path_to_chrome is None:
            if os.name == 'nt':
                # path_to_chrome = str(Path('./chromedriver.exe').relative_to('.'))
                path_to_chrome = str(Path('./ChromeDrivers/Windows/chromedriver.exe').absolute())
            elif os.name == 'darwin':
                path_to_chrome = str(Path('./ChromeDrivers/Mac/chromedriver').absolute())
            elif os.name == 'posix':
                path_to_chrome = str(Path('./ChromeDrivers/Linux/chromedriver').absolute())
            else:
                raise UnrecognizedOSError('Unable to recogized Operating System')

        self.browser = Chrome(path_to_chrome, options=options)

class CustomBrave(SeleniumAddons):

    def __init__(self, incognito=True, headless=False, disable_gpu=False) -> None:
        options = ChromeOptions()

        options.add_argument("disable-extensions")
        if incognito:
            options.add_argument("incognito")
        if headless:
            options.add_argument("headless")
        if disable_gpu:
            options.add_argument("disable-gpu")

        if os.name == 'nt':
            path_to_chrome = str(Path('./ChromeDrivers/Windows/chromedriver.exe').absolute())
            options.binary_location = str(Path('/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'))
        elif os.name == 'darwin':
            path_to_chrome = str(Path('./ChromeDrivers/Mac/chromedriver').absolute())
        elif os.name == 'posix':
            options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
            path_to_chrome = str(Path('./ChromeDrivers/Linux/chromedriver').absolute())
        else:
            raise UnrecognizedOSError('Unable to recogized Operating System')
        self.browser = Chrome(path_to_chrome, options=options)

class CustomFirefox(SeleniumAddons):

    def __init__(self, geckodriver_path=None, incognito=True, headless=False, service_log_path=None) -> None:
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
            #TODO: Test out this case
            raise UnrecognizedOSError('Selenium for Firefox not yet impliemented')
        else:
            raise UnrecognizedOSError('Unable to recogized Operating System')
        self.browser = Firefox(executable_path=geckodriver_path, options=options, service_log_path=service_log_path)



