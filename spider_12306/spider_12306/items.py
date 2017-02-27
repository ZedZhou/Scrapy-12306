# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#轮次
class TurnItem(scrapy.Item):
    id = scrapy.Field()
    mark = scrapy.Field()



#代售点
class AgencyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    province=scrapy.Field()
    name=scrapy.Field()
    address = scrapy.Field()
    start = scrapy.Field()
    # stop_time_am = scrapy.Field() 为了简便只取上午开始和下午结束时间
    # start_time_pm = scrapy.Field()
    end = scrapy.Field()
    windows = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    turn = scrapy.Field()

#铁路局信息
class StationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    turn = scrapy.Field()
    bureau=scrapy.Field()
    station=scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    passenger = scrapy.Field()
    luggage = scrapy.Field()
    package = scrapy.Field()


#列车时刻表信息
class InfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    turn = scrapy.Field()
    station_name =scrapy.Field()
    train_no=scrapy.Field()
    station_no=scrapy.Field()
    start_time = scrapy.Field()
    arrive_time = scrapy.Field()
    stopover_time = scrapy.Field()
    train_class_name = scrapy.Field()
 # 车站所对应 字母  XXX   
class CodeItem(scrapy.Item):
    turn = scrapy.Field()
    name = scrapy.Field()
    code = scrapy.Field()


class BriefItem(scrapy.Item):
    code = scrapy.Field()
    train_no = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    turn = scrapy.Field()


#列车 车号 和座位类型
class BriefDeltaItem(scrapy.Item):
    code = scrapy.Field()
    seat_type = scrapy.Field()
    turn = scrapy.Field()

#列车 座位票信息
class TicketItem(scrapy.Item):
    train_no = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    swz = scrapy.Field()
    tz = scrapy.Field()
    zy = scrapy.Field()
    ze = scrapy.Field()
    gr = scrapy.Field()
    rw = scrapy.Field()
    yw = scrapy.Field()
    rz = scrapy.Field()
    yz = scrapy.Field()
    wz = scrapy.Field()
    qt = scrapy.Field()
    turn = scrapy.Field()
   

class CommitItem(scrapy.Item):
    pass




