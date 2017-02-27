#coding:utf-8

#编写自己的过滤器, 对有 turn的url进行过滤
from scrapy.dupefilters import RFPDupeFilter
import logging
 
logger=logging.getLogger()

class MY_URLTurnFilter(RFPDupeFilter):
	def request_fingerprint(self,request):
		if 'turn' in request.meta:
			return request.url + ("-- %d" % request.meta['turn'])

		else:
			return request.url