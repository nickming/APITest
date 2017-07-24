#!/usr/bin/python
# -*- coding: utf-8 -*-
##日志输出类
import logging
import time
import os


def get_logger():
    global log_path
    try:
        log_path
    except NameError:
        log_path = os.path.abspath(os.getcwd())+'/data/logs/'
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file = log_path + time.strftime('%Y-%m-%d', time.localtime()) + '.log'
    if not os.path.exists(file):
        os.makedirs(log_path)
    logging.basicConfig(filename=file, level=logging.INFO, format=FORMAT)
    return logging
