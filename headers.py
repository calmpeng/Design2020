#!/usr/bin/env python
# -*- coding:utf-8 -*-      
#Author: pengxiang


import json


def get_headers_json(headers=None):
    if headers == None:
        headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
        Connection: keep-alive
        Cookie: __51cke__=; Hm_lvt_8edf227cc1aa2d220fae7d146a87c915=1583113830; PHPSESSID=kpbh4mfjl7jdn7apfrrl9kgms1; AnvVu_auth=ff9crWW2iL2RvjiaLZa5I6wwuScFrQ95TkuE38DNWay4Hq6Utpj44P2Te4uIVlRlrYy5X7auSZRP4PZ6NS6lJBLydjr4FhkhK1BEcBoEaBcOBlgCspsOgwgUeKtRWWVsTKWV0LWo31U2QcewTCSYfgFL5MQWlIA; AnvVu__userid=ff9crWW2iL2RvjiaLczoJ_5t6yYGqlohThqG3MWaBq3uQw; AnvVu__username=ff9crWW2iL2RvjiaLc2_c6g1vS0E_FhyGR2G2cP7Rw; AnvVu__groupid=ff9crWW2iL2RvjiaLZ7pJaVj73YNrw0mHkjW2cuZ; AnvVu__nickname=ff9crWW2iL2RvjiaLc2_c6g1vS0E_FhyGR2G2cP7Rw; __tins__19536543=%7B%22sid%22%3A%201583116771217%2C%20%22vd%22%3A%204%2C%20%22expires%22%3A%201583118585968%7D; __51laig__=15; Hm_lpvt_8edf227cc1aa2d220fae7d146a87c915=1583116786
        Host: www.cnpub.com.cn
        Referer: http://www.cnpub.com.cn/index.php?m=content&c=index&a=lists&catid=19&cbdi=%E6%9D%AD%E5%B7%9E&she=&times=&title=
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"""

    #headers = "\"" + headers.replace(": ", "\" : \"").replace("\n","\",\n\"")+"\""
    headers_json = {}
    for string in headers.split("\n"):
        string_temp = string.split(": ")
        headers_json.setdefault(string_temp[0].replace(" ",""), string_temp[1])
    return headers_json


