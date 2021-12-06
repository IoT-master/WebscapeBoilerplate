from Webscraper import CustomChrome
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':


    with CustomChrome(incognito=False) as web_scraper_with_context_manager:
        web_scraper_with_context_manager.browser.get('https://www.google.com')
        web_scraper_with_context_manager.wait_until_name_element_object_found('q')
        elem = web_scraper_with_context_manager.browser.find_element_by_name('q')
        elem.send_keys('hello')
        elem.send_keys(Keys.ENTER)

    with CustomFirefox(headless=True) as web_scraper_with_context_manager:
        web_scraper_with_context_manager.browser.get("https://www.google.com")
        elem = web_scraper_with_context_manager.browser.find_element(
            by=By.NAME, value="q"
        )
        elem.send_keys("hello")
        elem.send_keys(Keys.ENTER)

    #### This is how you would do it without Context Manager
    # web_scraper = CustomChrome(incognito=False)
    # web_scraper.browser.get('https://www.google.com')
    # web_scraper.wait_until_name_element_object_found('q')
    # elem = web_scraper.browser.find_element_by_name('q')
    # elem.send_keys('hello')
    # elem.send_keys(Keys.ENTER)
    # web_scraper.browser.close()