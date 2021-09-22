import os
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class CrawlJobs:
    def __init__(self):
        self.browser = None
        self.init_driver()

    def options_driver(self):
        CHROMEDRIVER_PATH = './chromedriver'
        WINDOW_SIZE = "1000,2000"
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument(
            '--disable-gpu') if os.name == 'nt' else None  # Windows workaround
        chrome_options.add_argument("--verbose")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument(
            "--disable-feature=IsolateOrigins,site-per-process")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--ignore-certificate-error-spki-list")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControllered")
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        # open Browser in maximized mode
        chrome_options.add_argument("--start-maximized")
        # overcome limited resource problems
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option(
            "prefs", {"profile.managed_default_content_settings.images": 2})
        chrome_options.add_argument('disable-infobars')
        chrome_options.page_load_strategy = 'none'
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                                  options=chrome_options
                                  )
        return driver

    def init_driver(self):
        self.browser = self.options_driver()

    def crawl(self):
        pass


if __name__ == '__main__':
    crawl_jobs = CrawlJobs()
    crawl_jobs.crawl()
