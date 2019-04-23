from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.parseUtil import *
from utils.code import *
from utils.webDriverUtil import *
import re
from urllib.parse import urlparse, unquote
import time
import random
from utils.dbUtil import *


class app:
    def __init__(self):
        self.driver = webDriverUtil.createWebDriver()
        self.db = dbUtil(DB_PATH)

    def login(self):
        self.driver.get(LOGIN_URL)
        username = self.driver.find_element_by_name('u')
        password = self.driver.find_element_by_name('p')
        username.send_keys(USER)
        password.send_keys(PASSWORD)
        self.driver.find_element_by_name('submit').send_keys(Keys.ENTER)
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "sitem"))
        )
        self.queue = self.db.getTaskUrl()
        for i in range(7):
            self.jumpToItemList(str(self.queue[0][1])+'&s=5&p=7'+str(i))

    def jumpToItemList(self,url):
        self.driver.get(url)
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
            postage = re.findall('postage_flg=[0-9]{1,}', itemTargetUrl)[0].replace('postage_flg=', '')
            data = {
                'itemTargetUrl': itemTargetUrl,
                'category': self.queue[0][2],
                'itemId': itemId,
                'title': title,
                'price': price,
                'shopName': shopName,
                'itemSaleUrl': itemSaleUrl,
                'postage':postage,
            }
            targetList.append(data)

        for target in targetList:
            # 判断是否存在
            if self.db.isSonzai(target['itemId']) == False:
                self.jumpToItemPage(target)
            else :
                print('跳过 '+str(itemId))
        self.db.endTask(self.queue[0][0], '成功')
        self.db.close()

    def jumpToItemPage(self, target):
        self.driver.get(target['itemTargetUrl'])
        codebox = self.driver.find_element_by_id(
            'codebox').get_attribute('value')
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
            target['category'],
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
            target['postage'],
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            0,
        ]
        addResultItemId = self.db.addItem(item4Add)
        if (addResultItemId != False):
            for imgUrl in imgList:
                imgUrl4Add = imgUrl.get_attribute('src')
                self.db.addImg(imgUrl4Add, addResultItemId)
        self.db.commit()
