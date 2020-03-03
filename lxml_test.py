#!/usr/bin/env python
# -*- coding:utf-8 -*-      
#Author: pengxiang


from lxml import etree

sample1 = """<html>
  <head>
    <title></title>
  </head>
  <body>
    <h2>Welcome to my <a href="#" src="x">page</a></h2>
    <p>This is the first paragraph.</p>
    <!-- this is the end -->
  </body>
</html>
"""

s1 = etree.HTML(sample1)
# 获取标题(两种方法都可以，第一种为绝对地址，第二种为相对地址)
print(s1)
print(s1.xpath('//title/text()'))  # 相对地址
print(s1.xpath('/html/head/title/text()'))  # 绝对地址
print(s1.xpath('//h2/a/@src'))
print(s1.xpath('//@href'))
print(s1.xpath('//text()'))  # 获取所有的文本
print(s1.xpath('//comment()'))  # 获取所有的注释

sample2 = """
<html>
  <body>
    <ul>
      <li>Quote 1</li>
      <li>Quote 2 with <a href="...">link</a></li>
      <li>Quote 3 with <a href="...">another link</a></li>
      <li><h2>Quote 4 title</h2> ...</li>
    </ul>
  </body>
</html>
"""
s2 = etree.HTML(sample2)
print(s2.xpath('//li/text()'))
print(s2.xpath('//li[1]/text()'))
print(s2.xpath('//li[a or h2]/text()'))
print(s2.xpath('//a/text()|//h2/text()'))

sample3 = """<html>
  <body>
    <ul>
      <li id="begin"><a href="https://scrapy.org">Scrapy</a>begin</li>
      <li><a href="https://scrapinghub.com">Scrapinghub</a></li>
      <li><a href="https://blog.scrapinghub.com">Scrapinghub Blog</a></li>
      <li id="end"><a href="http://quotes.toscrape.com">Quotes To Scrape</a>end</li>
      <li data-xxxx="end" abc="abc"><a href="http://quotes.toscrape.com">Quotes To Scrape</a>end</li>
    </ul>
  </body>
</html>
"""
s3 = etree.HTML(sample3)
print(s3.xpath('//li/a[@href = "https://scrapy.org"]/text()'))
print(s3.xpath('//li[@abc="abc"]/text()'))

from lxml import etree

sample4 = u"""
<html>
  <head>
    <title>My page</title>
  </head>
  <body>
    <h2>Welcome to my <a href="#" src="x">page</a></h2>
    <p>This is the first paragraph.</p>
    <p class="test">
    编程语言<a href="#">python</a>
    <img src="#" alt="test"/>javascript
    <a href="#"><strong>C#</strong>JAVA</a>
    </p>
    <p class="content-a">a</p>
    <p class="content-b">b</p>
    <p class="content-c">c</p>
    <p class="content-d">d</p>
    <p class="econtent-e">e</p>
    <p class="heh">f</p>
    <!-- this is the end -->
  </body>
</html>
"""
s4 = etree.HTML(sample4)
print(s4.xpath('string(//p[@class = "test"])'))  # 标签中的标签文本
print(s4.xpath('//p[contains(@class, "content")]/text()'))  # 包
