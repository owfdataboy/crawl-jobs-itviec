import os
import sys
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType


class CrawlJobs:
    def __init__(self, keys):
        self.browser = None
        self.HOME = 'https://itviec.com/'
        self.keys = keys
        self.init_driver()
        self.get_into_link(self.HOME)

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
        chrome_options.add_argument("user-agent=foo")
        # proxy
        PROXY = '171.244.10.43:2000'  # IP:PORT or HOST:PORT
        chrome_options.add_argument(f'--proxy-server={PROXY}')
        driver = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH, options=chrome_options)
        return driver

    def init_driver(self):
        self.browser = self.options_driver()

    def get_into_link(self, link):
        self.browser.get(link)

    def search_keyword(self, key):
        input = self.browser.find_element_by_class_name(
            'ui-autocomplete-input')
        input.send_keys(key)
        input.send_keys(Keys.ENTER)

    def refresh_home(self):
        self.get_into_link(self.HOME)

    def get_job_links(self):
        a_tags = self.browser.find_elements_by_xpath(
            "//a[contains(@target, '_blank') and contains(@data-controller, 'utm-tracking') and contains(@href, 'it-jobs')]")
        return [a.get_attribute('href') for a in a_tags]

    def next_page(self, i):
        link = f"//a[contains(@href, 'page={i}&source=search_job')]"
        button = self.browser.find_element_by_xpath(link)
        self.browser.execute_script("arguments[0].click();", button)

    def crawl(self):
        n = len(self.keys)
        for i in range(1, n):
            self.search_keyword(self.keys[i])
            job_links = self.get_job_links()
            print(len(job_links))
            try:
                i = 2
                while True:
                    self.next_page(i)
                    i += 1
                    sleep(2)
            except Exception as e:
                pass
            break
            self.refresh_home()
        sleep(10)
        self.browser.close()


if __name__ == '__main__':
    crawl_jobs = CrawlJobs(sys.argv)
    crawl_jobs.crawl()
