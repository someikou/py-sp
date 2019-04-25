import sqlite3
import time
from utils.logUtil import *

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

    def isSonzai(self,itemId):
        checkSql = "select id from items where item_id = '"+str(itemId)+"'"
        result = self.cursor.execute(checkSql).fetchall()
        if len(result) >= 1:
            return True
        return False

    def addItem(self,data,threadName):
        checkSql = "select id from items where item_id = '"+str(data[1])+"'"
        addSql = 'insert into items values ((select count(*)+1 from items),?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        result = self.cursor.execute(checkSql).fetchall()
        if len(result) >= 1:
            info(str(threadName) + '已经存在 ' + str(data[1]))
            return False
        else:
            self.cursor.execute(addSql,data)
            msg = '添加成功 ' if self.cursor.rowcount == 1 else '添加失败 '
            info(str(threadName) + str(msg) + str(data[1]))
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

    def getTaskUrl(self,threadName):
        getSql = "select id, url, category from queue where lock_flg = 0 and date(upd_time) < date('now') limit 1"
        result = self.cursor.execute(getSql).fetchall()
        if len(result) >= 1:
            prams = [
                '开始'+str(threadName),
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                result[0][0],
            ]
            lockSql = 'update queue set lock_flg = 1, biko = ? , upd_time = ? where id = ? and lock_flg = 0'
            lockResult = self.cursor.execute(lockSql,prams).rowcount
            if (lockResult == 1):
                self.conn.commit()
            else:
                self.getTaskUrl(threadName)
            # 有任务就返回任务信息
            return result
        else:
            # 没有任务
            return False
        

    def endTask(self,targetId,biko,threadName):
        prams = [
            biko+str(threadName),
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            targetId,
        ]
        unLockSql = 'update queue set lock_flg = 0, biko = ? , upd_time = ? where id = ?'
        result = self.cursor.execute(unLockSql, prams).fetchall()
        self.conn.commit()