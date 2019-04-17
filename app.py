from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.parseUtil import *
import re
from urllib.parse import urlparse,unquote

opts = webdriver.ChromeOptions()
opts.binary_location = 'C:\\Program Files (x86)\\Google\Chrome Beta\\Application\\chrome.exe'
driver = webdriver.Chrome(chrome_options = opts)
driver.implicitly_wait(10)
driver.set_window_size(360, 800)

testData = {
    'loginUrl':'',
    'username':'',
    'password':'',
    'itemList':'',
    'item':''
}

def login ():
    driver.get(testData['loginUrl'])
    username = driver.find_element_by_name('u')
    password = driver.find_element_by_name('p')
    username.send_keys(testData['username'])
    password.send_keys(testData['password'])
    driver.find_element_by_name('submit').send_keys(Keys.ENTER)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sitem"))
    )

def jumpToItemList () :
    driver.get(testData['itemList'])
    itemsList = driver.find_elements_by_css_selector('p[class="mb-2 mb-lg-3"] a')
    href = itemsList[0].get_attribute('href')
    print(href)
    targetList = []
    for item in itemsList:
        itemTargetUrl = item.get_attribute('href')
        itemId = re.findall('item_id=[a-zA-Z0-9_]{1,}',itemTargetUrl)[0].replace('item_id=','')
        price = re.findall('price=[a-zA-Z0-9_]{1,}',itemTargetUrl)[0].replace('price=','')
        title = unquote(re.findall('goods_name=[a-zA-Z0-9_\+\-.%]{1,}',itemTargetUrl)[0].replace('goods_name=',''))
        itemSaleUrl = unquote(re.findall('me_url=[a-zA-Z0-9_.\-%]{1,}',itemTargetUrl)[0].replace('me_url=',''))
        shopName = re.findall('co.jp/[a-zA-Z0-9_.\-%]{1,}',itemSaleUrl)[0].replace('co.jp/','')
        data = {
            'itemTargetUrl':itemTargetUrl,
            'itemId':itemId,
            'title':title,
            'price':price,
            'shopName':shopName,
            'itemSaleUrl':itemSaleUrl
        }
        targetList.append(data)

    for target in targetList:
        jumpToItemPage(target)

def jumpToItemPage(target):
    # driver.get(testData['item'])
    driver.get(target['itemTargetUrl'])
    codebox = driver.find_element_by_id('codebox').get_attribute('value')
    data = parseCodeBox(codebox)
    target['titleUrl'] = data['titleUrl']
    target['btnUrl'] = data['btnUrl']
    imgContainer = driver.find_element_by_id('alt_imgs_container')
    imgList = imgContainer.find_elements_by_class_name('p-1')
    imgUrlList = []
    for imgUrl in imgList:
        imgUrlList.append(imgUrl.get_attribute('src'))
    target['imgUrlList'] = imgUrlList
    # target['shopName'] = driver.find_element_by_id('shop_name').text
    target['shopUrl'] = driver.find_element_by_id('jump_url').get_attribute('href')
    target['shopMsg'] = driver.find_element_by_id('shop_blurb').text
    print(target['itemId'])
    print(target['title'])
    print(target['price'])
    print(target['shopName'])
    print(target['itemSaleUrl'])
    print(target['titleUrl'])
    print(target['btnUrl'])
    print(target['imgUrlList'][0])
    print(target['shopName'])
    print(target['shopUrl'])
    print(target['shopMsg'])

login()
# jumpToItemPage()
jumpToItemList()


