import os
import sys
import csv
import random
import traceback
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

    def get_proxy(self):
        proxies = ['171.244.10.43:2000']
        # return proxies[random.randint(0, len(proxies) - 1)]
        return proxies[0]

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
        PROXY = self.get_proxy()
        print(f'----------- Run project with: {PROXY}')
        chrome_options.add_argument(f'--proxy-server={PROXY}')
        driver = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH, options=chrome_options)
        return driver

    def init_driver(self):
        self.browser = self.options_driver()

    def write_csv(self, filename, content):
        with open(filename, 'a') as csvfile:
            csvobj = csv.writer(csvfile)
            csvobj.writerow(content)

    def get_into_link(self, link):
        self.browser.get(link)

    def search_keyword(self, key):
        input = self.browser.find_element_by_class_name(
            'ui-autocomplete-input')
        input.send_keys(key)
        input.send_keys(Keys.ENTER)
        sleep(1)

    def get_info_job(self):
        title = self.browser.find_element_by_class_name(
            'job-details__title').text
        try:
            reason = self.browser.find_element_by_class_name(
                'job-details__top-reason-to-join-us')
        except:
            reason = False
        tmp_title = self.browser.find_elements_by_class_name(
            'job-details__second-title')
        tmp = [reason] if reason else []
        paras = self.browser.find_elements_by_class_name(
            'job-details__paragraph')
        for p in paras:
            tmp.append(p)
        des = [" ".join((str1.text, str2.text))
               for (str1, str2) in zip(tmp_title, tmp)]
        return [title, des]

    def get_info_company(self):
        overview = self.browser.find_element_by_class_name(
            'job-details__overview').find_elements_by_class_name('svg-icon')
        address = overview[1].text
        date = overview[2].text
        com_name = self.browser.find_element_by_class_name(
            'employer-long-overview__name').text
        des = self.browser.find_element_by_class_name(
            'employer-long-overview__short-desc').text
        com_des = self.browser.find_element_by_class_name(
            'employer-long-overview__basic-info').text
        country = self.browser.find_element_by_class_name('svg-icon').text
        return [address, com_name, des, com_des, country, date]

    def get_details_job(self):
        return [*self.get_info_job(), *self.get_info_company()]

    def backto_previous_page(self, link):
        self.get_into_link(link)
        sleep(1)

    def refresh_home(self):
        self.get_into_link(self.HOME)

    def get_job_links(self):
        a_tags = self.browser.find_elements_by_xpath(
            "//a[contains(@target, '_blank') and contains(@data-controller, 'utm-tracking') and contains(@href, 'it-jobs')]")
        return [a.get_attribute('href') for a in a_tags]

    def next_page(self, i):
        link = f"//a[contains(@href, 'page={i}')]"
        button = self.browser.find_element_by_xpath(link)
        href = button.get_attribute('href')
        self.browser.execute_script("arguments[0].click();", button)
        return href

    def crawl(self):
        n = len(self.keys)
        for i in range(1, n):
            key_search = self.keys[i]
            print(f'##########################################################')
            print(f'----------- Processing job name: {key_search}')
            self.search_keyword(key_search)
            prev = f'https://itviec.com/it-jobs/{key_search}'
            try:
                i = 1
                while True:
                    job_links = self.get_job_links()
                    print(f'----------------------------------------------------------')
                    print(f'----------- Processing page: {i}')
                    print(
                        f'----------- Number of jobs per page: {len(job_links)}')
                    for job_i, job in enumerate(job_links):
                        print(f'----------- Processing job: {job_i + 1}')
                        self.get_into_link(job)
                        result = self.get_details_job()
                        self.write_csv(f'data/{key_search}-job.csv', result)
                        sleep(random.randint(1, 4))
                        break
                    i += 1
                    self.backto_previous_page(prev)
                    prev = self.next_page(i)
            except Exception as e:
                pass
            self.refresh_home()
        self.browser.close()


if __name__ == '__main__':
    crawl_jobs = CrawlJobs(sys.argv)
    crawl_jobs.crawl()
