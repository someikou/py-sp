from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform

class webDriverUtil:

    def createWebDriver():
        opts = webdriver.ChromeOptions()
        if (platform.system() != 'Darwin'):
            opts.binary_location = 'C:\\Program Files (x86)\\Google\Chrome Beta\\Application\\chrome.exe'
        opts.add_argument('headless') 
        # PROXY = 'scheme://user:pass@my.great.host:port'
        PROXY = '160.16.52.185:3128'
        opts.add_argument('--proxy-server=http://%s' % PROXY)
        driver = webdriver.Chrome(chrome_options = opts)
        # driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        driver.set_window_size(980, 800)
        return driver