from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
import zipfile

PROXY = '171.244.10.43:2000'  # IP:PORT or HOST:PORT

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--proxy-server={PROXY}')

chrome = webdriver.Chrome(options=chrome_options,
                          executable_path='./chromedriver')
chrome.get("http://whatismyipaddress.com")
