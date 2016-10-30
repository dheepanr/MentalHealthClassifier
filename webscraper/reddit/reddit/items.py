# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RedditItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comment_id = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    reply_type = scrapy.Field()
    conversation_resp = scrapy.Field()
    thread_starter = scrapy.Field()
    time = scrapy.Field()
    likes = scrapy.Field()
    comment = scrapy.Field()