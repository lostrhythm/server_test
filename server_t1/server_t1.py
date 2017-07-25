# -*- coding:utf-8 -*-
'''
Created on 2017年7月12日

@author: Thinkpad
'''
from flask import Flask
from flask import request
from log.log import get_logger
from server_methods_t1 import Server_Methods


logger = get_logger('server_t1', True)
Server_Methods_Ins = Server_Methods.from_default(logger)
app = Flask(__name__)



@app.route('/strategy', methods=['GET'])
def strategy_server():
    StrategyGroupJson = Server_Methods_Ins.get_strategy_t1()
    return StrategyGroupJson



@app.route('/task', methods=['POST'])
def task_server():
    TaskRequestJson = request.get_data() 
    TasksGroupJson = Server_Methods_Ins.get_task_t1(TaskRequestJson)
    return TasksGroupJson



@app.route('/upload', methods=['POST'])
def upload_server(): 
    UploadPackJson = request.get_data() 
    ComfirmInfo = Server_Methods_Ins.upload_result_t1(UploadPackJson)
    return ComfirmInfo



@app.route('/monitor', methods=['POST'])
def monitor_server():
    UserCollectorMapJson = request.get_data() 
    ComfirmInfo = Server_Methods_Ins.upload_status_t1(UserCollectorMapJson)
    return ComfirmInfo



@app.route('/register', methods=['POST'])
def register_server():
    UserInfoJson = request.get_data() 
    ComfirmInfo = Server_Methods_Ins.do_register_t1(UserInfoJson)
    return ComfirmInfo




if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)