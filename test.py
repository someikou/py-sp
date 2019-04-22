from utils.parseUtil import *
from utils.dbUtil import *
# codebox = open('codebox.html', mode='r', encoding='UTF-8')
# data = parseCodeBox(codebox)
# data['aaa'] = 'bbb'
# print(data['titleUrl'])
# print(data['aaa'])


db = dbUtil('./utils/afl.db')
db.getTaskUrl()
