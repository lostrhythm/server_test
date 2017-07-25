# -*- coding:utf-8 -*-
'''
Created on 2017年7月15日

@author: Thinkpad
'''
from threading import Thread
from log.log import get_logger
import time
import connection
from copy import deepcopy

CON = connection.get_myconn_from_default()
CUR = CON.cursor(
                 )
logger = get_logger('test_fill_mysql')


def reset_task_status_1():
    
    sqline = 'update Tasks set TaskStatus = -1 where TaskStatus = -2;'
    CUR.execute(sqline)
    logger.info('task status reseted -2 -> -1')
    

def reset_task_status_2():
    
    sqline_1 = 'update Tasks set TaskStatus = -2 where Processor is Null;'
    sqline_2 = 'update Tasks set TaskStatus = -3 where Processor is not Null;'
    CUR.execute(sqline_1)
    CUR.execute(sqline_2)
    logger.info('task status reseted -> -2 / -3')
    

def fill_new_tasks():
    sqline = "INSERT INTO Tasks (StrategyID, TaskContent) values ('TEST_%s', 'k1');"
    data = [(0,),(1,),(2,),(3,)] * 3
    while True:
        CUR.executemany(sqline, data)
        logger.info('new tasks filled: %s'%str(data))
        time.sleep(2)
        
    
    
def do_fill():
    t1 = Thread(target= fill_new_tasks)

    t1.start()

    
    
if __name__ == '__main__':

    sw_sign = raw_input('[1: reset_task_status_1, 2: reset_task_status_2, 3: fill_new_tasks]:')
    
    if sw_sign == '1':
        reset_task_status_1()
        
    elif sw_sign == '2':
        reset_task_status_2()
        
    elif sw_sign == '3':
        fill_new_tasks()
        
        
        
        