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
            self.mysql.insert_brand(brand)

    def save_series(self, item):
        # 保存父车系
        item = item.get('json')
        che168_parent_series_id = item['id']
        che168_parent_series_name = item['name']
        che168_brand_id = item.get('che168_brand_id')

        # 获取父车系在系统中所对应的品牌ID
        sys_brand = self.mysql.get_brand(che168_brand_id)
        print(' che168_brand_id = {0} 的 品牌为{1}'.format(che168_brand_id, sys_brand))

        # 判断系统中是否已存在该父车系 根据che168ID判断
        sys_series = self.mysql.get_parent_series(che168_parent_series_id)
        print(' che168_series_id = {0} 的 父车系为{1}'.format(che168_parent_series_id, sys_series))
        if not sys_series:
            save = (che168_parent_series_name, che168_parent_series_name, che168_parent_series_id, True, sys_brand[1],
                    sys_brand[0], 0,)
            sys_series_id = self.mysql.insert_parent_series(save)
        else:
            sys_series_id = sys_series[0]

        itemlist = item['seriesitems']

        ls = []
        for i in itemlist:
            che168_series_id = i.get('id')

            # 判断系统中是否已存在该子车系
            sys_child_series = self.mysql.get_series(che168_series_id)
            if sys_child_series:
                continue
            else:
                name = i.get('name')
                data = (
                    name, name, che168_series_id, True, sys_brand[1], sys_brand[0], i.get('seriesorder'), sys_series_id,
                    self.get_status(i.get('seriesstate')),)
                ls.append(data)

        if len(ls) > 0:
            self.mysql.insert_child_series(ls)

    def save_model(self, item):
        dic = item['json']
        che168_model_id = dic.get("specid")
        model = self.mysql.get_model(che168_model_id)
        if not model:
            model_name = dic.get("specname")
            body_type = dic.get("levelname")
            drive_mode = dic.get("specdrivingmodename")
            structure = dic.get("specstructuretypename")
            gearbox = dic.get("spectransmission")
            seat = dic.get("specstructureseat")
            engine = dic.get("specenginename")
            emission = dic.get('greenstandards')
            sys_brand_id = dic.get('sys_brand_id')
            sys_series_id = dic.get('sys_series_id')
            sys_brand_name = dic.get('sys_brand_name')
            sys_series_name = dic.get('sys_series_name')
            if seat:
                if not seat.isdigit():
                    seat = 4
            else:
                seat = 0
            data = (
                model_name, sys_brand_name, che168_model_id, True, sys_brand_name, sys_brand_id,
                sys_series_id,
                sys_series_name, body_type, gearbox, engine, structure, drive_mode, seat, emission,)
            model_id = self.mysql.insert_model(data)
        else:
            model_id = model[0]
        count = self.mysql.get_model_detail_count(model_id)
        if not count:
            self.save_model_detail(che168_model_id, model_id)
        else:
            print('------------------------------ 已存在model_id 为{0} 的详细参数 --------------------------------'.format(
                model_id))

    def save_model_detail(self, che_168_model_id, model_id):
        url = 'https://cars.app.autohome.com.cn/cfg_v7.0.0/cars/speccompare.ashx?pm=2&type=1&specids={0}'.format(
            che_168_model_id)
        res = requests.get(url=url)
        detail = json.loads(res.text)
        if detail.get('returncode') != 0:
            print('获取车型详细参数失败 {0}'.format(url))
            raise Exception('获取车型详细参数失败 {0}'.format(url))

        result = detail.get('result')
        params = result.get('paramitems')
        configs = result.get('configitems')
        ls = self.combine_sql(params, model_id)
        ls.extend(self.combine_sql(configs, model_id))
        self.mysql.insert_model_detail(ls)

    def get_status(self, status):
        status = int(status)
        if status == 20:
            return '在售'
        elif status == 30:
            return '停产在售'
        elif status == 40:
            return '停售'
        else:
            return '在售'

    def combine_sql(self, params, model_id):
        list = []
        for p in params:
            item_type = p.get("itemtype")
            for item in p.get('items'):
                name = item.get('name')
                value = item.get('modelexcessids')[0].get('value')

                if value:
                    is_num = value.isdigit()
                else:
                    is_num = False

                str_value = None
                num_value = None
                if (is_num):
                    num_value = value
                else:
                    str_value = value
                list.append((model_id, item_type, name, is_num, str_value, num_value,))
        return list
