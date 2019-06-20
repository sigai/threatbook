# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request
from redis import Redis

from threatbook.items import ThreatbookItem



class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['threatbook.cn']
    r = Redis(decode_responses=True)
    indices = ["ip", "tb-intelligence", "open-intelligence", "event", "sample", "url", 
                "reverseIpDomain", "ip/historyDomain", "ip/rdns",
                "ip/port",
                "ipSignature",
                "socialTag",
    ]
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "max-age=0",
            "cookie": "rememberme=af9258f58e67bfd0989074255546a6439a9736a6|vipfts@qq.com|1560946815799; islogin=undefined; VB_LANG=zh",
            "dnt": "1",
            "referer": "https://x.threatbook.cn/nodev4/vb4/article?threatInfoID=1625",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        },
    }
    
    def start_requests(self):
        members = self.r.smembers("threatbook:threat")
        for member in members:
            item = json.loads(member)
            if "IP" != item["ioc_type"]:
                continue
            ip = item["ioc_value"]
            for index in self.indices[:1]:
                url = f"https://x.threatbook.cn/nodev4/{index}/{ip}"
                yield Request(url, meta={"index": index}, dont_filter=True)
            break

    def parse(self, response):
        tb_tags = response.xpath('//div[@class="tag-info"]/div[@class="tag-list"]/div[contains(@class, "wb-tag")]/text()').extract()
        tags = [tag.strip() for tag in tb_tags]
        print(tags)
