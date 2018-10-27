# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from lxml import etree
import re,time
from weibo.items import ManItem

class ManSpider(scrapy.Spider):
    name = 'man'
    u = 'http://www.34jw.com'
    start_urls = ['http://www.34jw.com/html/part/20_13.html']

    def parse(self, response):
        file=open("d:\\m.html","w+")
        file.write(response.text)
        html=etree.parse("d:\\m.html",etree.HTMLParser())
        result=html.xpath("//a/@href")
        for i in result:
            result1=re.search("(^/html/article/.*html$)",str(i))
            if result1:
                new_url=self.u+result1.group(1)
                # print(new_url)
                yield Request(url=new_url,callback=self.detail_parse)

        next_result=re.search('.*(/html.*html).*下一页',response.text,re.S)
        if next_result:
            next_url=self.u+next_result.group(1)
 #           print("我是nexturl-----:",next_url)
            yield Request(url=next_url,callback=self.parse)
  #          time.sleep(3)
        else:
            print("next_result为空")


    def detail_parse(self,response):
        print("我是detail_parse,我请求的url是"+response.url)
        html=response.text
        urlresult=re.findall("<img src.*?(https://img6.26ts.com.*?\.jpg)",html,re.S)
        titlefind=re.findall("<title>(.*?)</title>",html,re.S)
        title=titlefind[0]
        if urlresult:
            for i in urlresult:
              #  print("-------jpgurl-------")
                item=ManItem()
                item["jpgurl"]=i
                item["title"]=title
                yield item
        else:
            print("为空！！！！")

