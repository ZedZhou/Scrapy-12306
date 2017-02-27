# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('/Users/Zed_zhou/Desktop/spider_12306/spider_12306')
from items import AgencyItem,CommitItem
import json
from scrapy.http.request import Request
import urllib

class AgencySpider(scrapy.Spider):
    name = "AgencySpider"

    

    #设置管道执行顺序
    custom_settings =  {
        #管道优先级
        'ITEM_PIPELINES':{
            'pipelines.Agency_mysql_pipeline':300
        },
        #去重日志
        # 'DUPEFILTER_DEBUG':True,
        #下载器中间件
        # 'DOWNLOADER_MIDDLEWARES':{
        # 'middlewares.DownloaderMiddleware':500,
        # },
        'DUPEFILTER_CLASS':'my_filter.MY_URLTurnFilter',

        #工作储存文件位置 
        # 'JOBDIR':'.....',

    }


    def __init__(self,*a,**kw):
        super(AgencySpider,self).__init__(self.name,**kw)
        self.turn = a[0]
        self.logger.info('%s. this turn %d' % (self.name,self.turn))

    def start_requests(self):
        yield Request('https://kyfw.12306.cn/otn/userCommon/allProvince',
            callback=self.parse,meta={'turn':self.turn})


    def parse(self, response):
        url='https://kyfw.12306.cn/otn/queryAgencySellTicket/query?'
        b=response.body
        r=json.loads(b)
        res=r['data']
        for pro in res:
            params={'province':pro['chineseName'].encode('utf-8'),'city':'','county':''}
            url_2=url+urllib.urlencode(params)
            yield Request(url=url_2,callback=self.parse_agency,
                meta={'turn':response.meta['turn']})

    def parse_agency(self,response):
        b=response.body
        r=json.loads(b)
        res=r['data']['datas']
        for i in res:
            item=AgencyItem()
            item["province"] = i["province"]
            item["city"] = i["city"]
            item["county"] = i["county"]
            item["address"] = i["address"]
            item["name"] = i["agency_name"]
            item["windows"] = i["windows_quantity"]
            item["start"] = i["start_time_am"]
            item["end"] = i["stop_time_pm"]
            item['turn'] = response.meta['turn']
            yield item

        yield CommitItem()
