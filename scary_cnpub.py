#!/usr/bin/env python
# -*- coding:utf-8 -*-      
#Author: pengxiang


import requests
import pickle
from lxml import etree
from headers import get_headers_json
import sys
import logging
import json

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE = "%m/%d/%Y %H:%M:%S %p "
logging.basicConfig(filename="scary_cnpub.log", filemode="a",level=logging.DEBUG,
                    format=LOG_FORMAT,datefmt=LOG_DATE)



# 中国图书出版数据库
main_url = "http://www.cnpub.com.cn"
url = "http://www.cnpub.com.cn/soushu.html"
headers = get_headers_json();
# 目标路径
target_form_url = "/html/body/div[3]/div[2]/div/form/@action"
target_publisher = "/html/body/div[3]/div[2]/div/form/div[4]/div[2]/ul/li/a/text()"
target_publisher_place = "/html/body/div[3]/div[2]/div/form/div[2]/div[2]/ul/li/a/text()"
target_publisher_time = "/html/body/div[3]/div[2]/div/form/div[6]/div[2]/ul/li/a/text()"

target_form_item = "//*[@name=\"searchform\"]/input/@name"
target_form_item_value = "//*[@name=\"searchform\"]/input/@value"
target_form_item_order = "//*[@name=\"searchform\"]/div[@class='men_qian1']/div[@class='men_qian_c']/ul/li/input/@name"



def cnpub_scary():
    response = requests.get(url=url, headers=headers,params="")
    response_string = response.content.decode("utf8")
    # 建立 html tree
    html_tree = etree.HTML(response_string)
    # 通过目标路径提取结点
    form_url = html_tree.xpath(target_form_url)
    publisher = html_tree.xpath(target_publisher)
    # 将 '不限' 剔除
    del publisher[0]
    publisher_time = html_tree.xpath(target_publisher_time)
    # 将 '不限' 剔除
    del publisher_time[0]
    publisher_place = html_tree.xpath(target_publisher_place)
    # 将 '不限' 剔除
    del publisher_place[0]
    form_item = html_tree.xpath(target_form_item)
    form_item_value = html_tree.xpath(target_form_item_value)
    form_item_order = html_tree.xpath(target_form_item_order)
    form = dict(zip(form_item,form_item_value))

    # 定一个 出版社
    form.setdefault(form_item_order[0], publisher_place[0])  # 地址
    form.setdefault(form_item_order[1], "")  # 出版社
    form.setdefault(form_item_order[2], "")  # 时间
    # form.setdefault("page", 1)

    response_search = requests.get(url=form_url[0], headers=headers, params=form)
    response_search_text = response_search.text
    html_tree_detail = etree.HTML(response_search_text)

    # 每本书的细节url
    # target_detail_url = "/html/body/div[3]/div[6]/div/div[1]/div/a[@target='_blank']/@href"
    # detail_url = html_tree_detail.xpath(target_detail_url)


    # 书本总数量
    target_detail_num = "/html/body/div[3]/div[6]/div/div[2]/ul/span[1]/text()"
    detail_num = html_tree_detail.xpath(target_detail_num)

    # 总页数
    target_detail_page = "/html/body/div[3]/div[6]/div/div[2]/ul/a[11]/text()"
    detail_page = html_tree_detail.xpath(target_detail_page)
    page = int(detail_page[0])
    # 制定一个出版地址的所有书本url
    one_publisher_allbook_url = []
    for i in range(page):
        form["page"] =  i

        response_search_i = requests.get(url=form_url[0],headers=headers,params=form)
        response_search_i_text = response_search_i.text

        # 每本书的细节url
        target_detail_url_i = "/html/body/div[3]/div[6]/div/div[1]/div/a[@target='_blank']/@href"
        html_tree_detail_i = etree.HTML(response_search_i_text)
        detail_url = html_tree_detail_i.xpath(target_detail_url_i)
        one_publisher_allbook_url.extend(detail_url)
        # if i > 5:
        #     break

    file = open("one_publisher_allbook_url", "wb")
    pickle.dump(one_publisher_allbook_url, file)
    file.close()


    book_lib = []
    for one_url in one_publisher_allbook_url:
        one_url = main_url + one_url
        book_lib.append(by_url_get_book_detail(one_url))
    return book_lib




def by_url_get_book_detail(url, headers=None):
    if headers == None:
        headers = get_headers_json()

    response = requests.get(url=url, headers=headers)
    response_tree = etree.HTML(response.content.decode("utf8"))
    book_detail_name = response_tree.xpath("/html/body/div[4]/div/div/div[1]/div[1]/div/div/div[3]/div[1]/h3/text()")
    #book_detail_autor = response_tree.xpath("/html/body/div[4]/div/div/div[1]/div[1]/div/div/div[3]/div[1]/p[1]/text()")
    book_detail_publish = response_tree.xpath("/html/body/div[4]/div/div/div[1]/div[1]/div/div/div[3]/div[1]/p[2]/a/text()")

    book_detal = response_tree.xpath("/html/body/div[4]/div/div/div[1]/div[1]/div/div/div[3]/div[1]/p/text()")

    try:
        if len(book_detail_publish) == 0:
            # 出版社没有 链接
            book_detail_publish = response_tree.xpath(
                "/html/body/div[4]/div/div/div[1]/div[1]/div/div/div[3]/div[1]/p[2]")

            # print(book_detail_publish[0].text)
            Temp = book_detail_publish[0].text
            TempStr = str(Temp).replace(" ","").split("：")
            book_detail_publish = TempStr[1][3:]


            book_detail_autor = book_detal[0]
            book_detail_cip = book_detal[2]
            book_detal_isbn = book_detal[3]
            book_deail_publish_place = book_detal[4]
            book_detail_publish_time = book_detal[5]
            book_detail_price = response_tree.xpath(
                "/html/body/div[4]/div/div/div[1]/div[1]/div/div/div[3]/div[1]/p/span/strong/text()")
        else:
            book_detail_publish = book_detail_publish[0]
            book_detail_autor = book_detal[0]
            book_detail_cip = book_detal[3]
            book_detal_isbn = book_detal[4]
            book_deail_publish_place = book_detal[5]
            book_detail_publish_time = book_detal[6]
            book_detail_price = response_tree.xpath(
                "/html/body/div[4]/div/div/div[1]/div[1]/div/div/div[3]/div[1]/p/span/strong/text()")

        context = response_tree.xpath("/html/body/div[4]/div/div/div[1]/div[3]/div[1]/p/text()")

        price =  str(book_detail_price[0])
        autor = str(book_detail_autor)
        autor_k_v = autor.split("：")  # 这里的： 是中文的
        cip = str(book_detail_cip)
        cip_k_v = cip.split("：")
        isbn = str(book_detal_isbn)
        isbn_k_v = isbn.split("：")
        publish_time = str(book_detail_publish_time)
        publish_time_k_v = publish_time.split("：")
        public_place = str(book_deail_publish_place)
        public_place_k_v = public_place.split("：")

        book = {}
        book.setdefault("name",book_detail_name[0])
        book.setdefault(autor_k_v[0],autor_k_v[1])
        book.setdefault("出版社",book_detail_publish)
        book.setdefault("name",book_detail_name)
        book.setdefault(cip_k_v[0],cip_k_v[1])
        book.setdefault(isbn_k_v[0],isbn_k_v[1].replace("-",""))
        book.setdefault(public_place_k_v[0],public_place_k_v[1])
        book.setdefault(publish_time_k_v[0],publish_time_k_v[1])
        book.setdefault("定价",price)
        book.setdefault("内容", context[0])
        book.setdefault("url",url)

        return book
    except :
        s = sys.exc_info()
        info = ("Error '%s' happened on line %d") % (s[1], s[2].tb_lineno)
        logging.debug("url" + url + str(sys.exc_info())+ str(info))


if __name__ == "__main__":
    book_lib = cnpub_scary()
    print(book_lib,book_lib.__len__())

    file = open("book_lib","wb")
    pickle.dump(book_lib,file)
    file.close()
    #
    # f = open('book_lib', 'rb')
    # book_lib = pickle.load(f)
    # print(book_lib)
    # f.close()


    #books = book_lib[0]
    #json.dump(books, open('./book_lib.txt', 'w'))
    # d = json.load(open('/tmp/result.txt','r'))

    #book = by_url_get_book_detail("http://www.cnpub.com.cn/tushu/2016/2017-01-09/46418.html")
    # book = by_url_get_book_detail("http://www.cnpub.com.cn/tushu/xueshu/2016-11-01/345.html")
    # print(book)