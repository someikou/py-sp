import sqlite3
import time

class dbUtil:
    
    def __init__(self,dbPath):
        self.conn = sqlite3.connect(dbPath)
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

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

    def addItem(self,data):
        checkSql = "select id from items where item_id = '"+str(data[0])+"'"
        addSql = 'insert into items values ((select count(*)+1 from items),?,?,?,?,?,?,?,?,?,?,?,?,?)'
        result = self.cursor.execute(checkSql).fetchall()
        if len(result) >= 1:
            msg = '已经存在 '+str(data[0])
            print(msg)
            return False
        else:
            self.cursor.execute(addSql,data)
            msg = '添加成功 ' if self.cursor.rowcount == 1 else '添加失败 '
            print(str(msg)+str(data[0])+': '+str(data[1]))
            return self.cursor.execute(checkSql).fetchall()[0][0]
    
    def addImg(self,imgUrl4Add,addResultItemId):
        data = [
            addResultItemId,
            imgUrl4Add,
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            0,
        ]
        addSql = 'insert into imgs values ((select count(*)+1 from imgs),?,?,?,?)'
        self.cursor.execute(addSql,data)

    def getTaskUrl(self):
        getSql = 'select id, url from queue where lock_flg = 0 limit 1'
        result = self.cursor.execute(getSql).fetchall()
        lockSql = 'update queue set lock_flg = 1 where id = '+str(result[0][0])
        lockResult = self.cursor.execute(lockSql).fetchall()
        self.conn.commit()
        return result

    def endTask(self,id,biko):
        prams = [
            biko,
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            id,
        ]
        unLockSql = 'update queue set lock_flg = 0, biko = ? , upd_time = ? where id = ?'
        self.cursor.execute(unLockSql, prams).fetchall()
        self.conn.commit()