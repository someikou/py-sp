from app import *
from utils.dbUtil import *
import threading,time

class myThread (threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):
        newApp = app()
        newApp.login()

# 创建新线程
thread1 = myThread(1, "Thread-1")
thread2 = myThread(2, "Thread-2")
thread3 = myThread(3, "Thread-3")
thread4 = myThread(4, "Thread-4")
thread5 = myThread(4, "Thread-4")

# 开启新线程
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()

print ("退出主线程")




