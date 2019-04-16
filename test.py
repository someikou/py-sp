from utils.parseUtil import *

codebox = open('codebox.html', mode='r', encoding='UTF-8')
data = parseCodeBox(codebox)
data['aaa'] = 'bbb'
print(data['titleUrl'])
print(data['aaa'])
