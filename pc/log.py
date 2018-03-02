# -*- encoding:utf-8 -*-
import logging

# create logger
logger_name = "example"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

# create file handler
log_path = "./log.log"
fh = logging.FileHandler(log_path)
fh.setLevel(logging.WARN)

# create formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

# add handler and formatter to logger
fh.setFormatter(formatter)
logger.addHandler(fh)

# print log info
logger.debug('debug dfasdf')
logger.info('info messaasdfasdfasdge')
logger.warn('warn message')
logger.error('error mesfasdsage')
logger.critical('criticalfasdfasdfasdf message')
'''

##### 文件配置
配置文件logging.conf如下:
```[loggers]
keys=root,example01

[logger_root]
level=DEBUG
handlers=hand01,hand02

[logger_example01]
handlers=hand01,hand02
qualname=example01
propagate=0

[handlers]
keys=hand01,hand02

[handler_hand01]
class=StreamHandler
level=INFO
formatter=form02
args=(sys.stderr,)

[handler_hand02]
class=FileHandler
level=DEBUG
formatter=form01
args=('log.log', 'a')

[formatters]
keys=form01,form02

[formatter_form01]
format=%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'''

#使用程序logger.py如下:
'''#!/usr/bin/python
# -*- encoding:utf-8 -*-
import logging
import logging.config

logging.config.fileConfig("./logging.conf")

# create logger
logger_name = "example"
logger = logging.getLogger(logger_name)

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')'''

