# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FunScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MeiTuItem(scrapy.Item):
    publisher = scrapy.Field()      # 出版商
    publishtime = scrapy.Field()    # 出版时间
    model_name = scrapy.Field()     # 模特姓名
    magazine_no = scrapy.Field()    # 期刊编号
    pic_qty = scrapy.Field()        # 图片数量
    pixel = scrapy.Field()          # 分辨率
    desc = scrapy.Field()           # 补充说明
    tag = scrapy.Field()            # 标签
    sort = scrapy.Field()           # 分类
    page_url = scrapy.Field()       # 被抓取页面URL
    image_url = scrapy.Field()      # 图片URL


