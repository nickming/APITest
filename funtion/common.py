#!/usr/bin/python
# -*- coding: utf-8 -*-

import core.core_logging as log
import constant
import core.core_request as request
import core.core_xls_tool as excel
from prettytable import PrettyTable

FILE_NAME = constant.FILE_NAME
logging = log.get_logger()


##数据准备
def prepare_data():
    logging.info('数据准备中')


# 数据从excel获取
def get_excel_sheet(path):
    excel.open_excel(path)
    return excel.get_sheet_by_index(0)


#转换数据为dict格式，进行post操作
def convert_data_to_dict(params, data):
    return {params: data}


# 数据测试
def run_test(sheet, url):
    rows = excel.get_rows(sheet)
    fail = 0
    for i in range(1, rows):
        test_data, test_method, test_name, test_number, test_params, test_url = get_content_from_excel(i, sheet, url)


        real_data = convert_data(test_data, test_method, test_params)

        test_code = excel.get_content(sheet, i, constant.CASE_CODE)
        actual_code = request.api_test(test_method, test_url, real_data)
        actual_code=int(actual_code)
        expect_code = test_code

        #处理错误信息
        failResults = handle_failed_result(actual_code, expect_code, real_data, test_method, test_number, test_url)
        if actual_code != expect_code:
            logging.info("测试失败 %s", test_name)
            print("失败信息")
            print(failResults)
            fail += 1
        else:
            logging.info("编号 %s", test_number)
            logging.info("测试名称 %s", test_name)
            logging.info('测试地址为:'+test_url)
            print("*******************************")
            print("编号: ",test_number)
            print("测试名称:",test_name)
            print("测试地址为: ",test_url)
            print("*******************************")
    if fail > 0:
        return False
    return True

#如果是post请求,则需要将请求封装为dict,get请求则可以将data置空,自行在params中写好字符串
def convert_data(test_data, test_method, test_params):
    if test_method == 'post':
        real_data = convert_data_to_dict(test_params, test_data)
    else:
        real_data = test_params
    return real_data

#从excel中获取字段数据
def get_content_from_excel(i, sheet, url):
    test_number = str(int(excel.get_content(sheet, i, constant.CASE_NUMBER)))
    test_name = str(excel.get_content(sheet, i, constant.CASE_NAME))
    test_params = str(excel.get_content(sheet, i, constant.CASE_PARAMS))
    test_data = str(excel.get_content(sheet, i, constant.CASE_DATA))
    test_url = excel.get_content(sheet, i, constant.CASE_URL)
    test_url = url + test_url
    test_method = excel.get_content(sheet, i, constant.CASE_METHOD)
    return test_data, test_method, test_name, test_number, test_params, test_url

#处理错误信息
def handle_failed_result(actual_code, expect_code, real_data, test_method, test_number, test_url):
    failResults = PrettyTable(["Number", "Method", "Url", "Data", "ActualCode", "ExpectCode"])
    failResults.align["Number"] = "l"
    failResults.padding_width = 1
    failResults.add_row([test_number, test_method, test_url, real_data, actual_code, expect_code])
    return failResults
