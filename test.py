from utils.parseUtil import *
from utils.dbUtil import *
from utils.webDriverUtil import *
import platform
# codebox = open('codebox.html', mode='r', encoding='UTF-8')
# data = parseCodeBox(codebox)
# data['aaa'] = 'bbb'
# print(data['titleUrl'])
# print(data['aaa'])

db = dbUtil('./utils/afl.db')
db.endTask(2,'seikoi2')

print(platform.system())

driverUtil = webDriverUtil(False)
driver = driverUtil.createWebDriver()
driverUtil.login()
driverUtil.get('https://tool.lu/ip/')
