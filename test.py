#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import core.core_logging as log
import funtion.common as common
import os

logging = log.get_logger()

url = sys.argv[1]  # 服务地址
count = int(sys.argv[2])  # 测试次数

logging.info("-------------- 开始测试 ---------------")

logging.info("获取测试用例数据解析")
sheet = common.get_excel_sheet(os.path.abspath(os.getcwd()) + common.FILE_NAME)

logging.info("数据解析准备")
common.prepare_data()

logging.info("测试用例执行中")
if len(sys.argv) == 1:
    res = common.run_test(sheet, url)
else:
    for i in range(count):
        temp=str(i)
        print("-------------- 第 "+temp+" 次测试开始---------------")
        logging.info("-------------- 第 %d 次测试---------------",i)
        res = common.run_test(sheet, url)
        print("-------------- 第 "+temp+" 次测试结束---------------")

logging.info("-------------- 获取测试结果 ------------ %s", res)
