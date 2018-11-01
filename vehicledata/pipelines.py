# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import requests

from vehicledata.items import VehicleBrand, VehicleSeries, VehicleModel, VehicleModelDetail
from vehicledata.utils import mysql


class VehicledataPipeline(object):

    def __init__(self):
        self.mysql = mysql()

    def process_item(self, item, spider):
        if isinstance(item, VehicleBrand):
            self.save_brand(item)
        elif isinstance(item, VehicleSeries):
            self.save_series(item)
        elif isinstance(item, VehicleModel):
            self.save_model(item)
            pass
        elif isinstance(item, VehicleModelDetail):
            print('VehicleModelDetail')
            pass

    def save_brand(self, itme):
        che168_id = itme['che_168_brand_id']
        if not self.mysql.get_brand(che168_id):
            brand = (itme['alias'], int(itme['che_168_brand_id']), itme['initial'], itme['name'], True)
            sys_brand = self.mysql.insert_brand(brand)
            print('*' * 40, '保存品牌{0}'.format(sys_brand[1]), '*' * 40)

    def save_series(self, item):
        item = item.get('json')
        che168_parent_series_id = item['id']
        che168_parent_series_name = item['name']
        che168_brand_id = item.get('che168_brand_id')

        sys_brand = self.mysql.get_brand(che168_brand_id)
        sys_series = self.mysql.get_parent_series(che168_parent_series_id)

        if not sys_series:
            save = (che168_parent_series_name, che168_parent_series_name, che168_parent_series_id, True, sys_brand[1],
                    sys_brand(0), 0,)

            sys_series = self.mysql.insert_parent_series(save)

        itemlist = item['seriesitems']

        ls = []
        for i in itemlist:
            che168_series_id = i.get('id')
            sys_series = self.mysql.get_series(che168_series_id)
            if sys_series:
                continue
            else:
                name = i.get('name')
                data = (
                    name, name, che168_series_id, True, sys_brand[1], sys_brand[0], i.get('seriesorder'), sys_series[0],
                    self.get_status(i.get('seriesstate')),)
                ls.append(data)

        if len(ls) > 0:
            self.mysql.insert_child_series(ls)

    def save_model(self, item):

        for i in item.get('json'):
            url = 'http://www.autohome.com.cn/ashx/ajaxoil.ashx?type=offical&specId={0}'.format(i.get('id'))
            response = requests.get(url=url)
            detail = json.loads(response.content.decode('gb2312'))
            print(detail)

    def get_status(self, status):
        if status == 20:
            return '在售'
        elif status == 30:
            return '停产在售'
        elif status == 40:
            return '停售'
        else:
            return '在售'
