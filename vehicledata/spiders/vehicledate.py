import json
import re

import scrapy

from vehicledata.items import VehicleBrand


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
        id = re.match(r'.+value=(\d+)', str(response.url), re.M | re.I).group()
        result.put('che168_brand_id', id)


if __name__ == '__main__':
    import scrapy.cmdline as line

    line.execute('scrapy crawl car'.split())
