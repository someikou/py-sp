from app import *
from utils.dbUtil import *
import threading,time
from utils.logUtil import *

class myThread (threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):
        newApp = app()
        newApp.login(self.name)

threadList = []
for i in range(2):
    count = i+1
    thread = myThread(count, "Thread-"+str(count))
    thread.start()
    threadList.append(thread)

for thread in threadList:
    thread.join()

info("退出主线程")




