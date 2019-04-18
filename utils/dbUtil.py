import sqlite3

class dbUtil:
    
    def __init__(self,dbPath):
        self.conn = sqlite3.connect(dbPath)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def getAllItems(self):
        #获取字段名称
        sql = 'pragma table_info(items)'
        self.cursor.execute(sql)
        parg = self.cursor.fetchall()
        col_names = [p[1] for p in parg] #获取字段名称

        result = self.cursor.execute('select * from items')
        for data in result:
            record = dict(zip(col_names, data))
            print(record['id'])
            print(data[1])

    def getNewId(self):
        result = self.cursor.execute('select count(*)+1 from items').fetchall()[0][0]
        return result

    def add(self,data):
        checkSql = "select id from items where item_id = '"+str(data[1])+"'"
        addSql = 'insert into items values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        result = self.cursor.execute(checkSql).fetchall()
        if len(result) >= 1:
            msg = '已经存在 '+str(data[1])
            print(msg)
        else:
            self.cursor.execute(addSql,data)
            self.conn.commit()
            msg = '添加成功 ' if self.cursor.rowcount == 1 else '添加失败 '
            print(str(msg)+str(data[0])+': '+str(data[2]))
        

# db = dbUtil('afl.db')
# item4Add = [
#     db.getNewId(),
#     '106180032',
#     'title',
#     'price',
#     'itemSaleUrl',
#     'titleUrl',
#     'btnUrl',
#     'imgAflUrl',
#     'imgShowAflUrl',
#     'imgUrlList',
#     6,
#     'shopName',
#     'shopUrl',
#     'shopMsg',
#     'upd_time',
#     0,
# ]
# print(item4Add[1])
# db.add(item4Add)
# db.commit()