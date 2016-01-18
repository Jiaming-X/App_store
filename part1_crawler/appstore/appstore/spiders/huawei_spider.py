# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from appstore.items import AppstoreItem

class HuaweiSpiderSpider(scrapy.Spider):
    name = "huawei"
    allowed_domains = ["huawei.com"]
    start_urls = (
        'http://appstore.huawei.com/more/all/1',
        'http://appstore.huawei.com/more/recommend/1',
        'http://appstore.huawei.com/more/soft/1',
        'http://appstore.huawei.com/more/game/1',
        'http://appstore.huawei.com/more/newPo/1',
        'http://appstore.huawei.com/more/newUp/1',
    )

    def parse(self, response):
      page = Selector(response)
      hrefs = page.xpath('//h4[@class="title"]/a/@href')

      for href in hrefs:
        url = href.extract()
        yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
      page = Selector(response)
      item = AppstoreItem()

      item['title'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()').extract_first().encode('utf-8')
      item['url'] = response.url
      item['appid'] = re.match(r'http://.*/(.*)', item['url']).group(1)
      item['intro'] = page.xpath('//meta[@name="description"]/@content').extract_first().encode('utf-8')

      divs = page.xpath('//div[@class="open-info"]')
      recomm = ""
      for div in divs:
        url = div.xpath('./p[@class="name"]/a/@href').extract_first()
        recommended_appid = re.match(r'http://.*/(.*)', url).group(1)
        name = div.xpath('./p[@class="name"]/a/text()').extract_first().encode('utf-8')
        recomm += "{0}:{1},".format(recommended_appid, name)
      item['recommended'] = recomm
      yield item      
