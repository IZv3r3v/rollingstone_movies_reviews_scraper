# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose
from w3lib.html import remove_tags

# Item representing movie review
class ReviewItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(lambda s: remove_tags(s).strip())
    )
    content = scrapy.Field(
        input_processor = lambda l: [remove_tags(e).strip() for e in l if not '<aside' in e], # sometimes aside element brakes html, so we need exclude them by hand
        output_processor = Join('\n')
    )
    date = scrapy.Field(
        input_processor = MapCompose(lambda s: remove_tags(s).strip())
    )
