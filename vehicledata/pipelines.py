# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import CloseSpider

from vehicledata.items import VehicleBrand, VehicleSeries, VehicleModel, VehicleModelDetail
from vehicledata.utils import mysql


class VehicledataPipeline(object):

    def __init__(self):
        self.mysql = mysql()

    def process_item(self, item, spider):
        if isinstance(item, VehicleBrand):
            self.save_brand(item)
        elif isinstance(item, VehicleSeries):
            print('VehicleSeries')
            pass
        elif isinstance(item, VehicleModel):
            print('VehicleModel')
            pass
        elif isinstance(item, VehicleModelDetail):
            print('VehicleModelDetail')
            pass

    def save_brand(self, itme):
        che168_id = itme['che_168_brand_id']
        if not self.mysql.get_brand(che168_id):
            brand = (itme['alias'], int(itme['che_168_brand_id']), itme['initial'], itme['name'], True)
            try:
                id = self.mysql.insert_brand(brand)
                print('*' * 40, '保存品牌{0}'.format(id), '*' * 40)
            except Exception as e:
                raise CloseSpider(reason="mysql出错")

    def parse_series(self, item):
        che168_parent_series_id = item['id']
        che168_parent_series_name = item['name']
        che168_parent_series_first_letter = item['firstletter']

        itemlist = item['seriesitems']
        for i in itemlist:
            che168_series_id = item['id']
            name = item['name']
            firstletter = item['firstletter']
            seriesorder = item['seriesorder']
