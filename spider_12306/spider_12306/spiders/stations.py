# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('/Users/Zed_zhou/Desktop/spider_12306/spider_12306')
from items import StationItem,CommitItem
import json
from scrapy.http.request import Request
import urllib

class StationsSpider(scrapy.Spider):
    name = "StationsSpider"

    
    #设置管道执行顺序
    custom_settings =  {
        #管道
        'ITEM_PIPELINES':{
            'pipelines.Station_mysql_pipeline':300
        },

        # 下载器中间件
        # 'DOWNLOADER_MIDDLEWARES':{
        # 'middlewares.DownloaderMiddleware':500,
        # },
        'DUPEFILTER_CLASS':'my_filter.MY_URLTurnFilter',
        'DUPEFILTER_DEBUG':True


    }


    def __init__(self,*a,**kw):
        super(StationsSpider,self).__init__(self.name,**kw)
        self.turn = a[0]
        self.logger.info('%s. this turn %d' % (self.name,self.turn))

    def start_requests(self):
        yield Request('http://www.12306.cn/mormhweb/kyyyz/',
            callback=self.parse,meta={'turn':self.turn})


    def parse(self, response):
        names=response.css('#secTable > tbody > tr > td::text').extract()
        sub_url=response.css('#mainTable td.submenu_bg > a::attr(href)').extract()
        for i in range(0,len(names)):

            #meta里的 station = True ---> 车站 
            sub_url1=response.url + sub_url[i*2][2:]
            yield Request(url=sub_url1,callback=self.parse_station,
                meta={'bureau':names[i],
                        'station':True,
                        'turn':response.meta['turn']
                        })

            #meta里的 station = False ---> 乘降所
            sub_url2=response.url + sub_url[i*2+1][2:]
            yield Request(url=sub_url2,callback=self.parse_station,
                meta={'bureau':names[i],
                        'station':False,
                        'turn':response.meta['turn']
                        })



    def parse_station(self,response):
        datas=response.css('table table tr')
        if len(datas) <= 2:
            return 
        for i in range(0,len(datas)):
            if i < 2:
                continue
            infos = datas[i].css('td::text').extract()
    
            item = StationItem()
            item["turn"] = response.meta["turn"]
            item["bureau"] = response.meta["bureau"]
            item["station"] = response.meta["station"]
            item["name"] = infos[0]
            item["address"] = infos[1]
            item["passenger"] = infos[2].strip() 
            item["luggage"] = infos[3].strip() 
            item["package"] = infos[4].strip() 
            yield item
 
        yield CommitItem()
