# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('/Users/Zed_zhou/Desktop/spider_12306/spider_12306')
from items import *
import json
from scrapy.http.request import Request
import urllib
import pymysql
import time
import datetime
class TicketInfoSpider(scrapy.Spider):
    name = "TicketInfoSpider"

    
    #设置管道执行顺序
    custom_settings =  {
        #管道优先级
        'ITEM_PIPELINES':{
            'pipelines.ticket_info_mysql_pipeline':300
        },
        
        #下载器中间件
        # 'DOWNLOADER_MIDDLEWARES':{
        # 'middlewares.DownloaderMiddleware':500,
        # },
        #去重
        'DUPEFILTER_DEBUG':True,
        'DUPEFILTER_CLASS':'my_filter.MY_URLTurnFilter',

        #工作储存文件位置 
        # 'JOBDIR':'s/ticket_info',

    }


    def __init__(self,*a,**kw):
        super(TicketInfoSpider,self).__init__(self.name,**kw)
        self.turn = a[0]
        self.logger.info('%s. this turn %d' % (self.name,self.turn))

    def start_requests(self):
        yield Request('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8936',
            callback=self.parse,meta={'turn':self.turn})



    @staticmethod
    def fetch_routes():
        conn = pymysql.connect(host = 'localhost',
                                    port = 3306,
                                    user = '12306',
                                    passwd = '12306',
                                    db = '12306_train',
                                    charset = 'utf8')


        select = "select * from train_infos"


        schedules = {}
        with conn.cursor() as cursor:
            cursor.execute(select)
            count = 0
            for results in cursor.fetchall():
                if results[0] not in schedules:
                    schedules[results[0]] = {results[1]:results[2]}
                else:
                    schedules[results[0]][results[1]] = results[2]


        routes = {}
        for key in schedules:
            route = schedules[key]

            seq = sorted(route)
            len1 = len(seq)
            for i in range(0, len1):
                if route[seq[i]] not in routes:
                    tmp = set()
                    routes[route[seq[i]]] = tmp
                else:
                    tmp = routes[route[seq[i]]]
                for j in range(i + 1, len1):
                    tmp.add(route[seq[j]])
        return routes




    def parse(self, response):

        station_doc = response.body.decode('utf-8')
        stations = station_doc.split(u'@')
        results = {}
        #获取站点 代号 XXX
        for i in range(0,len(stations)):
            if '|' in stations[i]:
                station=stations[i].split('|')
                results[station[1]]=station[2]
                item=CodeItem()
                item['name']=station[1]
                item['code']=station[2]
                item['turn']=response.meta['turn']
                yield item

        yield CommitItem()
        #调用静态方法
        routes = TicketInfoSpider.fetch_routes()

        url='https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&'


        'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=24000000T70W&from_station_no=01&to_station_no=13&seat_types=1413&train_date=2016-11-15'

        t=(datetime.datetime.now()+datetime.timedelta(days=2))
        print t
        res=(str(t).split(' '))
        # date 为查询时间
        date=res[0]


        for s in routes:
            if s in results:
                code_s = results[s]
            else:
                self.logger.warning("code miss " + s)
                continue
            for e in routes[s]:
                if e in results:
                    code_e = results[e]
                else:
                    self.logger.warning("code miss " + e)
                    continue
                 
            params = u"queryDate=" + date + u"&from_station=" + code_s + u"&to_station=" + code_e

            yield Request(url + params,callback=self.parse_ticket_infos,
                        meta={'s':s,'e':e,'turn':response.meta['turn']
                        })



    #列车信息， 座位余票信息
    def parse_ticket_infos(self,response):
        datas = json.loads(response.body)

        if 'datas' not in datas['data']:
            self.logger.info('no data' + response.meta['s'] + response.meta['e'])
            return 

        for data in datas['data']['datas']:
            deltaItem = BriefDeltaItem()

            deltaItem["code"] = data["station_train_code"]
            deltaItem["seat_type"] = data["seat_types"]
            deltaItem["turn"] = response.meta["turn"]
            yield deltaItem

            item = TicketItem()
            item["train_no"] = data["train_no"]
            item["start"] = data["from_station_name"]
            item["end"] = data["to_station_name"]
            item["swz"] = data["swz_num"]
            item["turn"] = response.meta["turn"]

            #各种座位余票
            if item["swz"] == '--':
                item["swz"] = -1
            item["tz"] = data["tz_num"]
            if item["tz"] == '--':
                item["tz"] = -1
            item["zy"] = data["zy_num"]
            if item["zy"] == '--':
                item["zy"] = -1
            item["ze"] = data["ze_num"]
            if item["ze"] == '--':
                item["ze"] = -1
            item["gr"] = data["gr_num"]
            if item["gr"] == '--':
                item["gr"] = -1
            item["rw"] = data["rw_num"]
            if item["rw"] == '--':
                item["rw"] = -1
            item["yw"] = data["yw_num"]
            if item["yw"] == '--':
                item["yw"] = -1
            item["rz"] = data["rz_num"]
            if item["rz"] == '--':
                item["rz"] = -1
            item["yz"] = data["yz_num"]
            if item["yz"] == '--':
                item["yz"] = -1
            item["wz"] = data["wz_num"]
            if item["wz"] == '--':
                item["wz"] = -1
            item["qt"] = data["qt_num"]
            if item["qt"] == '--':
                item["qt"] = -1
                
            yield item

        yield CommitItem()



























