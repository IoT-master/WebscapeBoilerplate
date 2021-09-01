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
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException
from pathlib import Path
import os
from abc import ABC


class UnrecognizedOSError(NotImplementedError):
    pass


class ElementNotFound(Exception):
    pass


class SimpleLocator:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, browser):
        try:
            return browser.find_element(*self.locator).is_displayed()
        except NoSuchElementException:
            return False


class Clickable:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, browser):
        try:
            return browser.find_element(*self.locator).is_enabled()
        except StaleElementReferenceException:
            return False
        except ElementNotInteractableException:
            return False


class SeleniumAddons(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.browser = WebDriver()

    def highlight_element(self, element, border='1', border_color='red', bg_color='yellow'):
        s = f"background: {bg_color}; border: {border}px solid {border_color};"
        driver = element._parent
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);", element, s)

    def drag_and_drop(self, source_element_object, destination_element_object):
        ActionChains(self.browser).drag_and_drop(
            source_element_object, destination_element_object).perform()

    def scroll_and_moves_mouse_to(self, element_object):
        ActionChains(self.browser).move_to_element(element_object).perform()

    def scroll_to(self, lines_down, lines_right=0):
        self.browser.execute_script(
            f"window.scrollTo({lines_right}, {lines_down})")

    def scroll_to_element_location(self, element_object):
        coord = element_object.location
        self.browser.execute_script(
            "window.scrollTo(arguments[0], arguments[1]);", coord['x'], coord['y'])

    def scroll_into_view(self, element_object):
        self.browser.execute_script(
            "arguments[0].scrollIntoView();", element_object)

    def is_present(self, element_object):
        try:
            if element_object.is_displayed():
                return True
        except:
            return False

    def update_browser(self):
        for handle in self.browser.window_handles:
            self.browser.switch_to.window(handle)

    def wait_for_possible_element(self, partial_dom, locator, wait_time=10):
        wait = WebDriverWait(partial_dom, wait_time)
        wait.until(SimpleLocator(locator))

    def wait_until_css_element_object_found(self, partial_dom, css_param, wait_time=10):
        wait = WebDriverWait(partial_dom, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, css_param)))

    def wait_until_css_elements_object_found(self, partial_dom, css_param_list, wait_time=10):
        wait = WebDriverWait(partial_dom, wait_time)
        for css_param in css_param_list:
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, css_param)))

    def wait_until_css_element_object_is_clickable(self, partial_dom, css_param, wait_time=10):
        wait = WebDriverWait(partial_dom, wait_time)
        wait.until(Clickable((By.CSS_SELECTOR, css_param)))

    def wait_until_name_element_object_found(self, partial_dom, name_param, wait_time=10):
        wait = WebDriverWait(partial_dom, wait_time)
        wait.until(EC.visibility_of_element_located((By.NAME, name_param)))

    def wait_until_partial_link_text_element_object_found(self, partial_dom, partial_link_text, wait_time=10):
        wait = WebDriverWait(partial_dom, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, partial_link_text)))

    def wait_until_class_name_element_object_found(self, partial_dom, class_name, wait_time=10):
        wait = WebDriverWait(partial_dom, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, class_name)))

    def wait_until_id_element_object_found(self, partial_dom, id_object, wait_time=10):
        wait = WebDriverWait(partial_dom, wait_time)
        wait.until(EC.visibility_of_element_located((By.ID, id_object)))

    def wait_until_partial_link_text_object_found(self, partial_dom, id_object, wait_time=10):
        wait = WebDriverWait(partial_dom, wait_time)
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

    def __exit__(self, *args):
        print('Closing browser instance')
        self.browser.quit()


class CustomChrome(SeleniumAddons):

    def __init__(self, incognito=True, path_to_chrome=None, headless=False, disable_gpu=False, window_size=False, disable_extensions=True) -> None:
        options = ChromeOptions()

        # https://stackoverflow.com/questions/64927909/failed-to-read-descriptor-from-node-connection-a-device-attached-to-the-system
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        if disable_extensions:
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
                path_to_chrome = str(
                    Path('./ChromeDrivers/Windows/chromedriver.exe').absolute())
            elif os.name == 'darwin':
                path_to_chrome = str(
                    Path('./ChromeDrivers/Mac/chromedriver').absolute())
            elif os.name == 'posix':
                path_to_chrome = str(
                    Path('./ChromeDrivers/Linux/chromedriver').absolute())
            else:
                raise UnrecognizedOSError(
                    'Unable to recogized Operating System')

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
            path_to_chrome = str(
                Path('./ChromeDrivers/Windows/chromedriver.exe').absolute())
            options.binary_location = str(
                Path('/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'))
        elif os.name == 'darwin':
            path_to_chrome = str(
                Path('./ChromeDrivers/Mac/chromedriver').absolute())
        elif os.name == 'posix':
            options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
            path_to_chrome = str(
                Path('./ChromeDrivers/Linux/chromedriver').absolute())
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
                geckodriver_path = str(
                    Path('./FirefoxDrivers/Windows/geckodriver.exe').absolute())
            if service_log_path is None:
                service_log_path = str(
                    Path('./FirefoxDrivers/Windows/gecko.log').absolute())
        elif os.name == 'posix':
            # TODO: Test out this case
            raise UnrecognizedOSError(
                'Selenium for Firefox not yet impliemented')
        else:
            raise UnrecognizedOSError('Unable to recogized Operating System')
        self.browser = Firefox(executable_path=geckodriver_path,
                               options=options, service_log_path=service_log_path)
