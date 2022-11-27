import sys
import logging.handlers

LogFormat = '%(asctime)s-%(levelname)s-%(message)s'
logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format=LogFormat
)


def getFileLogger(name):
    logger = logging.getLogger(name)
    handler = logging.handlers.TimedRotatingFileHandler('/tmp/%s.log' % name, when='D', interval=1, backupCount=7, encoding='utf-8')
    handler.suffix = "%Y%m%d"
    formatter = logging.Formatter(LogFormat)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
