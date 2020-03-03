#!/usr/bin/env python
# -*- coding:utf-8 -*-      
#Author: pengxiang


import sys
import logging
# form = {}
# form.setdefault("page", 1)
# form.setdefault("page", 2)
# form["page"] = 3
# print(form)

str = "123abcrunoob321"
print(str.strip( '12' ))  # 字符序列为 12


str = "\r\n\t中"
# str.replace("\t","")
print(str[3:])
# str.strip('\r\n\t')
#
# string = str.splitlines()
# print(string)

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE = "%m/%d/%Y %H:%M:%S %p "
logging.basicConfig(filename="test.log", filemode="a",level=logging.DEBUG,
                    format=LOG_FORMAT,datefmt=LOG_DATE)


a = [1]
try:
    if a[3] == 0:
        a[3] = 12
        print(a)
except:
    s = sys.exc_info()
    info = ("Error '%s' happened on line %d") % (s[1], s[2].tb_lineno)
    logging.debug("123")
