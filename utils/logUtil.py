import logging,time
# DEBUG	详细信息，一般只在调试问题时使用。
# INFO	证明事情按预期工作。
# WARNING	某些没有预料到的事件的提示，或者在将来可能会出现的问题提示。例如：磁盘空间不足。但是软件还是会照常运行。
# ERROR	由于更严重的问题，软件已不能执行一些功能了。
# CRITICAL	严重错误，表明软件已不能继续运行了。
logFileName = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.log'
logging.basicConfig(
    handlers=[logging.FileHandler(logFileName, encoding="utf-8")],
    level=logging.INFO#控制台打印的日志级别
    #filemode='a'#模式，有w(重写)和a(续写)，
    #format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    )

def info(param):
    logging.info(param)
    