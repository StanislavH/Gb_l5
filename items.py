import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    sal_from = scrapy.Field()
    sal_to = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    pass
