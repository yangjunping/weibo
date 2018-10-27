# -*- coding: utf-8 -*-
from scrapy import Request
import scrapy
import json
import re,time
from scrapy import Item
from weibo.items import WeiboItem
class FansSpider(scrapy.Spider):
    name = 'fans'
    #allowed_domains = ['https://m.weibo.cn/']
    start_urls = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    def start_requests(self):
        yield Request(self.start_urls.format(uid="5648507852",page="2"),callback=self.detail_parse)
    def get_deatail(self):

        pass
    def getItem(self,card):
        for j in range(len(card)):
            card_group = card[j]
            item = WeiboItem()
            desc1 = card_group.get("desc1")
            desc2 = card_group.get("desc2")
            id = card_group.get('user').get("id")
            name = card_group.get('user').get("screen_name")
            item['name'] = name
            item['weiboid'] = id
            item["desc1"] = desc1
            item["desc2"] = desc2
            return item

    def judge_parse(self,response):
        result = json.loads(response.text)
        if result.get("ok"):
            print("初步判断ok")
            card_group = result.get("data").get("cards")
            if len(card_group)>6:           #判断是否是第一页，如果是：
                site=len(card_group)-1         #第一页cards列表只有最后一项提取数据
                card_group = result.get("data").get("cards")[site].get("card_group")
                idcode = result.get("data").get("cardlistInfo").get("containerid")
                nextpage = result.get("data").get("cardlistInfo").get("page")
                print("我还没提取", idcode)
                print("nextpage-------------------------",nextpage)
                if idcode:
                    result = re.match("^231051.*?(\d+)", idcode)
                    idcode = result.group(1)
                    print("idcode------------------------",idcode)
                yield Request(self.start_urls.format(uid=str(idcode),page=str(nextpage)),callback=self.detail_parse)
                for i in range(len(card_group)):
                    item = WeiboItem()
                    desc1 = card_group[i].get("desc1")
                    desc2 = card_group[i].get("desc2")
                    # print(card_group[i].get("user"))
                    id = card_group[i].get('user').get("id")
                    name = card_group[i].get('user').get("screen_name")
                    item['name'] = name
                    item['weiboid'] = id
                    item['desc1'] = desc1
                    item['desc2'] = desc2
                    print("*******i am id ***************:",id)
                    yield item
            #    yield Request(self.start_urls.format(uid=str(id), page="1"), callback=self.judge_parse)
                    #返回一个个新的id，第一页的请求


            else:
                print("i have come here-----------------------------------------")
                yield Request(url=response.url,callback=self.detail_parse)
        else:
            print("同一个ID以下已经全部爬完")
            current_url=response.url
            first_url=re.sub(".*?page=(\d+)","1",current_url)

    def detail_parse(self, response):
        result = json.loads(response.text)
        if result.get("ok")==0:
            print("同一个ID以下已经全部爬完")
        else:
            idcode = result.get("data").get("cardlistInfo").get("containerid")
            nextpage = result.get("data").get("cardlistInfo").get("page")
            print("我还没提取", idcode)
            if idcode:
                result1 = re.match("^231051.*?(\d+)", idcode)
                idcode = result1.group(1)

            print("-----------------------------------------")
            print("nextpage:",nextpage)
            print("------------------------------------------")
            card=result.get("data").get("cards")[0].get("card_group")
            item=self.getItem(card)
            if item:
                yield item
                yield Request(self.start_urls.format(uid=str(idcode), page=str(nextpage)), callback=self.detail_parse)
              #  yield Request(self.start_urls.format(uid=str(id),page="1"),callback=self.judge_parse)


    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     pass


