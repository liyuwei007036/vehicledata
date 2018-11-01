import json
import re

import scrapy

from vehicledata.items import VehicleBrand, VehicleSeries, VehicleModel
from vehicledata.utils import mysql


class Vehicle(scrapy.Spider):
    name = "car"

    def start_requests(self):
        url = 'http://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=1'
        yield scrapy.Request(url=url, callback=self.parse_brand, dont_filter=True)

    def parse_brand(self, response):
        dic = json.loads(response.text)
        result = dic.get('result').get('branditems')
        for i in result:
            item = VehicleBrand()
            item['che_168_brand_id'] = i.get('id')
            item['name'] = i.get('name')
            item['alias'] = i.get('name')
            item['initial'] = i.get('bfirstletter')
            url = 'http://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=3&value={0}'.format(i.get('id'))
            yield item
            yield scrapy.Request(url=url, callback=self.parse_series, dont_filter=True)

    def parse_series(self, response):
        dic = json.loads(response.text)
        result = dic.get('result')
        id = re.match(r'.+value=(\d+)', str(response.url), re.M | re.I).group(1)
        for i in result.get('factoryitems'):
            item = VehicleSeries()
            i['che168_brand_id'] = id
            item['json'] = i
            yield item
            for j in i.get('seriesitems'):
                che168_series_id = j.get('id')
                # 根据车系ID获取车型
                url = 'http://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=5&value={0}'.format(che168_series_id)
                yield scrapy.Request(url=url, callback=self.parse_model, dont_filter=True)

    def parse_model(self, response):
        dic = json.loads(response.text)
        result = dic.get('result').get('yearitems')
        series_id = re.match(r'.+value=(\d+)', str(response.url), re.M | re.I).group(1)

        series_info = mysql().get_series_info(series_id)

        for m in result:
            # 取得
            l = m.get('specitems')
            for mo in l:
                mo['che168_series_id'] = series_id
                url = 'http://www.autohome.com.cn/ashx/ajaxoil.ashx?type=offical&specId={0}'.format(mo.get('id'))
                yield scrapy.Request(url=url, callback=self.parse_model2, dont_filter=True,
                                     meta={'series_info': series_info})

    def parse_model2(self, response):
        series_info = response.request.meta['series_info']
        dic = json.loads(response.text)
        res = dic.get('result')
        res['sys_brand_id'] = series_info[2]
        res['sys_brand_name'] = series_info[3]
        res['sys_series_id'] = series_info[0]
        res['sys_series_name'] = series_info[1]
        item = VehicleModel()
        item['json'] = res
        yield item


if __name__ == '__main__':
    import scrapy.cmdline as line
    from datetime import datetime
    today = datetime.now()
    line.execute('scrapy crawl car -s LOG_FILE=d:\che168brand-{0}-{1}-{2}-log.log'.format(today.year, today.month, today.day).split())
