from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

opts = webdriver.ChromeOptions()
opts.binary_location = 'C:\\Program Files (x86)\\Google\Chrome Beta\\Application\\chrome.exe'
driver = webdriver.Chrome(chrome_options = opts)
driver.implicitly_wait(10)
driver.set_window_size(360, 800)

data = {
    'loginUrl':'https://grp02.id.rakuten.co.jp/rms/nid/vc?__event=login&service_id=p11',
    'username':'',
    'password':'',
    'item':"https://affiliate.rakuten.co.jp/link/pc/item?me_id=1193666&item_id=10044582&me_url=https%3A%2F%2Fitem.rakuten.co.jp%2Fvehicle%2F33000008%2F&me_img_src=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Fvehicle%2Fcabinet%2Fgios%2F2019%2F33000008.jpg&goods_name=%E3%83%AD%E3%83%BC%E3%83%89%E3%83%AC%E3%83%BC%E3%82%B5%E3%83%BC+2019+GIOS+%E3%82%B8%E3%82%AA%E3%82%B9+FURBO+%E3%83%95%E3%83%AB%E3%83%9C+%E3%82%B8%E3%82%AA%E3%82%B9%E3%83%96%E3%83%AB%E3%83%BC&mitem_flg=1&price=95040&tax_flg=0&postage_flg=0&change_flg=0"
}
driver.get(data['loginUrl'])
username = driver.find_element_by_name('u')
password = driver.find_element_by_name('p')
username.send_keys(data['username'])
password.send_keys(data['password'])
driver.find_element_by_name('submit').send_keys(Keys.ENTER)

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "sitem"))
)
driver.get(data['item'])
codebox = driver.find_element_by_id('codebox')
print(codebox.get_attribute('value'))



