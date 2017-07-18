# -*- coding:utf-8 -*-
'''
Created on 2017年6月19日

@author: Thinkpad
'''
import logging
import os
from logging import handlers


def get_logger(LOG_FILE_NAME = 'test', KeepRecord = False):    
    fmt = '%(asctime)s - %(filename)s:%(lineno)s [%(name)s] %(message)s'  
    formatter = logging.Formatter(fmt)   # 实例化formatter  
    
    
    logger = logging.getLogger(LOG_FILE_NAME)    # 获取名为tst的logger
    logger.setLevel(logging.DEBUG)
    
    '''handlers'''
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if KeepRecord:
        if not os.path.isdir('./logs'): # when run the spider in root dir, the logs dir will also be created there
            os.mkdir('./logs')
            
        LOG_FILE = './logs/' + LOG_FILE_NAME + '.log' 
        
        file_handler = handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler  
        file_handler.setFormatter(formatter)      # 为handler添加formatter   
        logger.addHandler(file_handler)      # 为logger添加handler
    ''''''
        
    return logger


if __name__ == '__main__':
    logger = get_logger('test')
    logger.info('first info message')  
    logger.debug('first debug message')  

