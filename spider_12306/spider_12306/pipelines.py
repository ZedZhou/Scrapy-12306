# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymysql.cursors
import sys
sys.path.append('/Users/Zed_zhou/Desktop/spider_12306/spider_12306')

from .items import *


#
class Agency_mysql_pipeline(object):
    def __init__(self):
        self.conn=pymysql.connect(host='localhost',port=3306,
                                  user='12306',password='12306',
                                  db='12306_train',charset='utf8')
        self.cursor=self.conn.cursor()
        self.sql = "INSERT IGNORE INTO agencys(province, city,\
                county, address, name, windows,\
                start, end,turn) VALUES\
                (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
    def process_item(self,item,spider):
        if isinstance(item, CommitItem):
            print '失败'
            self.conn.commit()
        else:
            print '插入数据~~~~~~~~~~~~~~~'
            self.cursor.execute(self.sql, (item["province"], item["city"],
                item["county"], item["address"],
                item["name"], item["windows"],
                item["start"] + u"00",
                item["end"] + u"00",
                item['turn']))
        

class Station_mysql_pipeline(object):
    def __init__(self):

        self.conn = pymysql.connect(host = 'localhost', port = 3306, 
                                        user = '12306',
                                        password = '12306',
                                        db = '12306_train',
                                        charset = 'utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT IGNORE INTO `stations` (`bureau`, `station`,\
                `name`, `address`, `passenger`, `luggage`,\
                `package`, `turn`) VALUES\
                (%s, %s, %s, %s, %s, %s, %s, %s)"
    def process_item(self,item,spider):
        if isinstance(item,CommitItem):
            self.conn.commit()
        else:
            print '储存 Station -----------------------'
            self.cursor.execute(self.sql,(item["bureau"], item["station"],
                item["name"], item["address"],
                item["passenger"], item["luggage"],
                item["package"], item["turn"]))

#列车时刻表。。。
class train_info_mysql_pipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', port = 3306, 
                                        user = '12306',
                                        password = '12306',
                                        db = '12306_train',
                                        charset = 'utf8')
        self.cursor = self.conn.cursor()
        self.brief_sql = "INSERT IGNORE INTO train_briefs VALUES\
                    (%s, %s, %s, %s, null, %s)"
        self.info_sql = "INSERT IGNORE INTO train_infos VALUES\
                    (%s, %s, %s, %s, %s, %s, %s)"
        self.turn_sql = "INSERT IGNORE INTO turns VALUES\
                    (%s, %s)"

    def process_item(self, item, spider):
        try:
            if isinstance(item, CommitItem):
                self.conn.commit()

            #处理BriefItem
            elif isinstance(item, BriefItem):
                print '储存 BriefItem -----------------------'
                self.cursor.execute(self.brief_sql, (item["code"], 
                    item["train_no"],
                    item["start"], item["end"], item["turn"]))
            #处理InfoItem
            else:
                print '储存 InfoItem -----------------------'
                self.cursor.execute(self.info_sql, (
                    item["train_no"],
                    item["station_no"],
                    item['station_name'],
                    item["start_time"], item["arrive_time"],
                    item["stopover_time"], item["turn"]))
        except Exception, e:
            spider.logger.warning("excute sql failed.")
            spider.logger.warning(str(e))
#余票信息
class ticket_info_mysql_pipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', port = 3306, 
                                        user = '12306',
                                        password = '12306',
                                        db = '12306_train',
                                        charset = 'utf8')
        self.cursor = self.conn.cursor()
        self.update_brief = "UPDATE train_briefs SET \
                    seat_type = %s WHERE code = %s and turn = %s"
        self.station_sql = "INSERT IGNORE INTO `train_stations` VALUES\
                    (%s, %s, %s)"
        self.tickets_sql = "INSERT IGNORE INTO train_tickets VALUES\
                    (%s, %s, %s, %s, %s, %s, %s, %s,\
                    %s, %s, %s, %s, %s, %s, %s)"

    def process_item(self, item, spider):
        try:
            if isinstance(item, CommitItem):
                self.conn.commit()
            elif isinstance(item, BriefDeltaItem):
                self.cursor.execute(self.update_brief, (item["seat_type"], 
                    item["code"], item["turn"]))
            elif isinstance(item, CodeItem):
                self.cursor.execute(self.station_sql, (item["name"], 
                    item["code"], item["turn"]))
            #储存列车信息，座位余票信息
            else:
                print '储存余票信息--------------------'
                self.cursor.execute(self.tickets_sql, (item["train_no"],
                    item["start"], item["end"], item["swz"],
                    item["tz"], item["zy"], item["ze"],
                    item["gr"], item["rw"], item["yw"],
                    item["rz"], item["yz"], item["wz"],
                    item["qt"], item["turn"]))
        except Exception, e:
            spider.logger.warning("excute sql failed.")
            spider.logger.warning(str(e))
        











































