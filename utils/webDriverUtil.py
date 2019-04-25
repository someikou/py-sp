from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
from utils.code import *
from utils.logUtil import *

class webDriverUtil:

    def __init__(self,headless):
        self.counter = 1
        
        self.opts = webdriver.ChromeOptions()
        if (platform.system() != 'Darwin'):
            self.opts.binary_location = 'C:\\Program Files (x86)\\Google\Chrome Beta\\Application\\chrome.exe'
        if headless:
            self.opts.add_argument('headless')
        self.setNewIp()

    def setNewIp(self):
        # PROXY = 'scheme://user:pass@my.great.host:port'
        PROXY = '133.167.81.162:8080'
        self.opts.add_argument('--proxy-server=http://%s' % PROXY)

    def createWebDriver(self):
        self.driver = webdriver.Chrome(chrome_options = self.opts)
        # driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(980, 800)
        return self.driver

    def login(self):
        self.get(LOGIN_URL)
        username = self.driver.find_element_by_name('u')
        password = self.driver.find_element_by_name('p')
        username.send_keys(USER)
        password.send_keys(PASSWORD)
        self.driver.find_element_by_name('submit').send_keys(Keys.ENTER)
        element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "sitem"))
        )

    def get(self,url):
        try: 
            self.driver.get(url)
        except Exception as e:
            # 最多切换3次线路
            self.driver.quit()
            if "-32000" in e.__str__() and self.counter < 4 :
                self.counter = self.counter + 1
                info('切换线路')
                self.setNewIp()
                self.createWebDriver()
                self.login()
                self.get(url)
            else:
                info('网络不正常')