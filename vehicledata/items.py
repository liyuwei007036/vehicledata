# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VehicleBrand(scrapy.Item):
    name = scrapy.Field()
    alias = scrapy.Field()
    initial = scrapy.Field()
    che_168_brand_id = scrapy.Field()


class VehicleSeries(scrapy.Item):
    # id = scrapy.Field()
    # name = scrapy.Field()
    # parent = scrapy.Field()
    # parent_id = scrapy.Field()
    # brand = scrapy.Field()
    # brand_id = scrapy.Field()
    # brand_name = scrapy.Field()
    # link_url = scrapy.Field()
    # alias = scrapy.Field()
    # photo = scrapy.Field()
    # sort_order = scrapy.Field()
    # recommended = scrapy.Field()
    # status = scrapy.Field()
    # valid = scrapy.Field()
    # che168_series_id = scrapy.Field()
    jsonArray = scrapy.Field()


class VehicleModel(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    brand_id = scrapy.Field()
    brand_name = scrapy.Field()
    series_id = scrapy.Field()
    series_name = scrapy.Field()
    alias = scrapy.Field()
    che168_model_id = scrapy.Field()
    start_date = scrapy.Field()
    stop_date = scrapy.Field()
    factory_price = scrapy.Field()
    price_history = scrapy.Field()
    recommended = scrapy.Field()
    country = scrapy.Field()
    body_type = scrapy.Field()
    gearbox = scrapy.Field()
    engine = scrapy.Field()
    volume = scrapy.Field()
    fuel = scrapy.Field()
    imported = scrapy.Field()
    structure = scrapy.Field()
    drive_mode = scrapy.Field()
    seat = scrapy.Field()
    emission = scrapy.Field()


class VehicleModelDetail(scrapy.Item):
    id = scrapy.Field()
    model_id = scrapy.Field()
    type = scrapy.Field()
    property = scrapy.Field()
    string_value = scrapy.Field()
    is_number = scrapy.Field()
    number_value = scrapy.Field()
