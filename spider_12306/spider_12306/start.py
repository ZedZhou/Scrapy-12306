# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime

import pymysql.cursors

project_path = os.path.dirname(os.path.abspath(__file__ + "/.."))
sys.path.insert(0, project_path)

import sys
sys.path.append('/Users/Zed_zhou/Desktop/spider_12306/spider_12306')


# import the spiders you want to run
from spiders.Agency import AgencySpider
from spiders.stations import StationsSpider
from spiders.trains_info import train_info_Spider 
from spiders.ticket_info import TicketInfoSpider

# scrapy api imports
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

crawler = CrawlerProcess(settings)

def sleep(secs):
    d = defer.Deferred()
    reactor.callLater(secs, d.callback, None)
    return d

@defer.inlineCallbacks
def crawl():

    conn = pymysql.connect(host = 'localhost', port = 3306, 
                                    user = '12306',
                                    password = '12306',
                                    db = '12306_train',
                                    charset = 'utf8')

    # agency_count = 30
    # station_count = 30
    # train_count = 5
    # ticket_count = 1
    # first = True

    # last_turn = -1
    # while True:
    n = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    s = time.time()
    turn = int(s / 86400)

    # if turn == last_turn:
    #     sleep(5)
    #     continue

    # print "new turn", turn, n
    # last_turn = turn

    with conn.cursor() as cursor:
        cursor.execute("INSERT IGNORE INTO `turns` VALUES (%s, %s)", (turn, n))
    conn.commit()
    conn.close()

    yield crawler.crawl(AgencySpider, turn)
    # yield crawler.crawl(StationsSpider, turn)
    # yield crawler.crawl(train_info_Spider, turn)
    # yield crawler.crawl(TicketInfoSpider, turn)

    print "crawler over"

# 设置去重时间间隔，
#         if first or turn % agency_count == 0:
#             yield crawler.crawl(AgencySpider, turn)
#         if first or turn % station_count == 0:
#             yield crawler.crawl(StationsSpider, turn)
#         if first or turn % train_count == 0:
#             yield crawler.crawl(train_info_Spider, turn)
#         if first or turn % ticket_count == 0:
#             yield crawler.crawl(TicketInfoSpider, turn)

#         first = False
#         e = time.time()
#         left = int(86400 - e + s)

#         if left > 0:
#             print "sleep", left
#             sleep(left)


crawl()
crawler.start()


