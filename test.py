from utils.parseUtil import *
from utils.dbUtil import *
import platform
# codebox = open('codebox.html', mode='r', encoding='UTF-8')
# data = parseCodeBox(codebox)
# data['aaa'] = 'bbb'
# print(data['titleUrl'])
# print(data['aaa'])


# db = dbUtil('./utils/afl.db')
# db.endTask(2,'seikoi2')

# print(platform.system())


for i in range(5):
    target = 'XXXXX'
    print(str(target)+str('&s=5&p=')+str(i))