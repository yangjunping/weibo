# -*- coding: utf-8 -*-
from scrapy import Request
import scrapy
import json
from scrapy import Item
from weibo.items import WeiboItem
class FansSpider(scrapy.Spider):
    name = 'fans'
#    allowed_domains = ['https://m.weibo.cn/']
    start_urls = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    def start_requests(self):
        yield Request(self.start_urls.format(uid="1879241531",page="2"),callback=self.parse)

    def detail_parese(self,response):
        pass
    def parse(self, response):
        result=json.loads(response.text)
        for j in range(20):
            card_group=result.get("data").get("cards")[j].get("card_group")
            for i in range(len(card_group)):
                item=WeiboItem()
                desc1=card_group[i].get("desc1")
                desc2=card_group[i].get("desc2")
                id=card_group[i].get('user').get("id")
                name=card_group[i].get('user').get("screen_name")
                item['name'] = name
                item['weiboid']=id
                item["desc1"]=desc1
                item["desc2"]=desc2
                if item:
                    yield item
                    yield Request(self.start_urls.format(uid=id,page="2"),callback=self.parse)



