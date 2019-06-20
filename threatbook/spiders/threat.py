# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from redis import Redis

from threatbook.items import ThreatbookItem



class ThreatSpider(scrapy.Spider):
    name = 'threat'
    allowed_domains = ['threatbook.cn']
    r = Redis(decode_responses=True)
    
    def start_requests(self):
        for i in range(1000, 1700):
            url = f"https://x.threatbook.cn/nodev4/vb4/article?threatInfoID={i}"
            yield Request(url, dont_filter=True)

    def parse(self, response):
        ips = response.xpath('//a[starts-with(@href, "/nodev4/ip/")]/text()').extract()
        domains = response.xpath('//a[starts-with(@href, "/nodev4/domain/")]/text()').extract()
        for ip in ips:
            yield ThreatbookItem(ioc_type="IP", ioc_value=ip)
        for domain in domains:
            yield ThreatbookItem(ioc_type="Domain", ioc_value=domain)
