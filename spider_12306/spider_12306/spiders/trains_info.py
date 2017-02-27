# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('/Users/Zed_zhou/Desktop/spider_12306/spider_12306')
from items import BriefItem,InfoItem,CommitItem,TurnItem
import json
from scrapy.http.request import Request
import urllib
import datetime
import time

class train_info_Spider(scrapy.Spider):
    name = "train_info_Spider"

    
    #设置管道执行顺序
    custom_settings =  {
        #管道优先级
        'ITEM_PIPELINES':{
            'pipelines.train_info_mysql_pipeline':300
        },
        'DUPEFILTER_DEBUG':True,
        #下载器中间件
        # 'DOWNLOADER_MIDDLEWARES':{
        # 'middlewares.DownloaderMiddleware':500,
        # },
        'DUPEFILTER_CLASS':'my_filter.MY_URLTurnFilter',

        #工作储存文件位置
        # 'JOBDIR':'s/train_info',

    }


    def __init__(self,*a,**kw):
        super(train_info_Spider,self).__init__(self.name,**kw)
        self.turn = a[0]
        self.logger.info('%s. this turn %d' % (self.name,self.turn))

    def start_requests(self):

        t=(datetime.datetime.now()+datetime.timedelta(days=2))

        print t
        res=(str(t).split(' '))
        date=res[0]
        url='https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?'
        params={'date':date}
        #将 params通过urllib.urlencode添加到  url中
        url_2=url+urllib.urlencode(params)

        yield Request(url_2,callback=self.parse,
            meta={'t':date,'turn':self.turn})






    def parse(self, response):
        s=json.loads(response.body)
        datas=s['data']
        url='https://kyfw.12306.cn/otn/czxx/queryByTrainNo?'
        for data in datas:
            item=BriefItem()
            briefs=data['station_train_code'].split('(')
            item['code']=briefs[0]
            briefs = briefs[1].split('-')
            item['start']=briefs[0]
            item['end']=briefs[1][:-1]
            item['train_no'] = data['train_no']
            item['turn'] = response.meta['turn']
            yield item
            params = u'train_no=' + data['train_no'] + u'&from_station_telecode=BBB&to_station_telecode=BBB&depart_date=' + response.meta["t"]
           


            yield Request(url=url+params,callback=self.parse_train_infos,
                meta={'train_no':data['train_no'],
                        'turn':response.meta['turn']
                        })



    #列车时刻表，只需要知道train_no和date  城市代码用BBB代替即可
    def parse_train_infos(self,response):

        s=json.loads(response.body)
        datas=s['data']['data']
        for i in range(0, len(datas)):

            data=datas[i]
            item=InfoItem()
            item['train_no']=response.meta['train_no']
            item['station_no']=data['station_no']
            item['station_name']=data['station_name']
            item['turn'] = response.meta['turn']
            if data['start_time'] == u'----':
                item['start_time']=None

            else:
                item['start_time']=data['start_time']+u':00'

			
            if data['arrive_time'] == u'----':
                item['arrive_time']=None
            else:
                item['arrive_time']=data['arrive_time']+u':00'


            if data['stopover_time'] == u'----':
                item['stopover_time']=None
            else:
                item['stopover_time']=data['stopover_time']+u':00'

            yield item

        yield CommitItem()




