#!/usr/bin/env python
# -*- coding:utf-8 -*-      
#Author: pengxiang

import requests
from headers import get_headers_json

url = 'http://www.cnpub.com.cn/index.php?m=content&c=index&a=lists&catid=19&cbdi=%E6%9D%AD%E5%B7%9E&she=&times=&title=&page=1'
response = requests.get(url=url)
print(response.content)