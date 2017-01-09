# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import log
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader, Identity
from ..items import MeiTuItem

class MeiTuSpider(scrapy.spiders.Spider):
    name = 'MeiTu'
    allowed_domains = ["meitulu.com"]
    homepage = "http://www.meitulu.com"
    links = []

    def __init__(self, sort="guochan", *args, **kwargs):
        super(MeiTuSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://www.meitulu.com/%s" % sort]
        log.msg("开始抓取 ..." , level=log.INFO)

    def parse(self, response):
        log.msg("正在解析列表页面: %s ..." % response.url, level=log.INFO)
        select = Selector(response)

        # 解析要抓取的套图页面
        for group in select.xpath("//ul[@class='img']/li/a/@href").extract():
            request = scrapy.Request(group, callback=self.parse_page)
            yield request

        # 获取列表的下一页
        next_page = select.xpath("//center/div[@class='text-c']/a[@class='a1'][2]/@href").extract()
        request = scrapy.Request(''.join([self.homepage, next_page[0]]), callback=self.parse)
        if request.url != response.url:
            yield request

    def parse_page(self, response):
        log.msg("正在解析套图页面: %s ..." % response.url, level=log.INFO)
        select = Selector(response)
        # 抓取当前套图页面
        request = scrapy.Request(response.url, callback=self.parse_image, dont_filter=True)
        yield request


        next_page = select.xpath("//center/div[@id='pages']/a[@class='a1'][2]/@href").extract()
        request = scrapy.Request(next_page[0], callback=self.parse_page)
        if request.url != response.url:
            yield request

    def parse_image(self, response):
        log.msg("正在收集页面数据: %s ..." % response.url, level=log.INFO)
        loader = ItemLoader(item=MeiTuItem(), response=response)

        loader.add_xpath('publisher', "//div[@class='width']/div[@class='c_l']/p[1]/text()")
        loader.add_xpath('publisher', "//div[@class='width']/div[@class='c_l']/p[1]/a[@class='tags']/text()")
        loader.add_xpath('model_name', "//div[@class='width']/div[@class='c_l']/p[5]/text()")
        loader.add_xpath('model_name', "//div[@class='width']/div[@class='c_l']/p[5]/a[@class='tags']/text()")
        loader.add_xpath('publishtime', "//div[@class='width']/div[@class='c_l']/p[6]/text()")
        loader.add_xpath('magazine_no', "//div[@class='width']/div[@class='c_l']/p[2]/text()")
        loader.add_xpath('pic_qty', "//div[@class='width']/div[@class='c_l']/p[3]/text()")
        loader.add_xpath('pixel', "//div[@class='width']/div[@class='c_l']/p[4]/text()")

        try:
            loader.add_xpath('desc', "//p[@class='buchongshuoming'/text()]")
        except ValueError:
            pass

        loader.add_xpath('tag', "//div[@class='fenxiang_l']/a[@class='tags']/text()")
        loader.add_xpath('sort', "//div[@class='weizhi']/span/a[2]/text()")
        loader.add_xpath('image_url', "//div[@class='content']/center/img[@class='content_img']/@src")
        loader.add_value("page_url", response.url)


        yield loader.load_item()