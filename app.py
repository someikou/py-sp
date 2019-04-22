from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.parseUtil import *
import re
from urllib.parse import urlparse, unquote
import time
import random
from utils.dbUtil import *

class app:
    def __init__(self):
        self.opts = webdriver.ChromeOptions()
        self.opts.binary_location = 'C:\\Program Files (x86)\\Google\Chrome Beta\\Application\\chrome.exe'
        self.opts.add_argument('headless')  # 静默模式
        self.driver = webdriver.Chrome(chrome_options=self.opts)
        # self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(360, 800)
        self.testData = {
            'loginUrl': '',
            'username': '',
            'password': '',
            'itemList': '',
            'item': ''
        }
        time.sleep(random.randint(1, 5))
        self.db = dbUtil('./utils/afl.db')

    def login(self):
        self.driver.get(self.testData['loginUrl'])
        username = self.driver.find_element_by_name('u')
        password = self.driver.find_element_by_name('p')
        username.send_keys(self.testData['username'])
        password.send_keys(self.testData['password'])
        self.driver.find_element_by_name('submit').send_keys(Keys.ENTER)
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "sitem"))
        )

    def jumpToItemList(self):
        self.queue = self.db.getTaskUrl()
        self.driver.get(self.queue[0][1])
        itemsList = self.driver.find_elements_by_css_selector(
            'p[class="mb-2 mb-lg-3"] a')
        href = itemsList[0].get_attribute('href')
        print(href)
        targetList = []
        for item in itemsList:
            itemTargetUrl = item.get_attribute('href')
            itemId = re.findall(
                'item_id=[a-zA-Z0-9_]{1,}', itemTargetUrl)[0].replace('item_id=', '')
            price = re.findall(
                'price=[a-zA-Z0-9_]{1,}', itemTargetUrl)[0].replace('price=', '')
            title = unquote(re.findall(
                'goods_name=[a-zA-Z0-9_\+\-.%]{1,}', itemTargetUrl)[0].replace('goods_name=', ''))
            itemSaleUrl = unquote(re.findall(
                'me_url=[a-zA-Z0-9_.\-%]{1,}', itemTargetUrl)[0].replace('me_url=', ''))
            shopName = re.findall(
                'co.jp/[a-zA-Z0-9_.\-%]{1,}', itemSaleUrl)[0].replace('co.jp/', '')
            data = {
                'itemTargetUrl': itemTargetUrl,
                'itemId': itemId,
                'title': title,
                'price': price,
                'shopName': shopName,
                'itemSaleUrl': itemSaleUrl
            }
            targetList.append(data)

        for target in targetList:
            time.sleep(random.randint(1, 5))
            self.jumpToItemPage(target)
        self.db.endTask(self.queue[0][0],'成功')
        self.db.close()

    def jumpToItemPage(self,target):
        # self.driver.get(self.testData['item'])
        self.driver.get(target['itemTargetUrl'])
        codebox = self.driver.find_element_by_id('codebox').get_attribute('value')
        data = parseCodeBox(codebox)
        target['titleUrl'] = data['titleUrl']
        target['btnUrl'] = data['btnUrl']
        target['imgAflUrl'] = data['imgAflUrl']
        target['imgShowAflUrl'] = data['imgShowAflUrl']
        imgContainer = self.driver.find_element_by_id('alt_imgs_container')
        imgList = imgContainer.find_elements_by_class_name('p-1')
        # target['shopName'] = self.driver.find_element_by_id('shop_name').text
        target['shopUrl'] = self.driver.find_element_by_id(
            'jump_url').get_attribute('href')
        target['shopMsg'] = self.driver.find_element_by_id('shop_blurb').text
        item4Add = [
            target['itemId'],
            target['title'],
            target['price'],
            target['itemSaleUrl'],
            target['titleUrl'],
            target['btnUrl'],
            target['imgAflUrl'],
            target['imgShowAflUrl'],
            target['shopName'],
            target['shopUrl'],
            target['shopMsg'],
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            0,
        ]
        addResultItemId = self.db.addItem(item4Add)
        if (addResultItemId != False):
            for imgUrl in imgList:
                imgUrl4Add = imgUrl.get_attribute('src')
                self.db.addImg(imgUrl4Add, addResultItemId)
        self.db.commit()
