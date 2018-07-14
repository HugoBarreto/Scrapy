# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from re import sub, search

class LivroPipeline(object):
    def process_item(self, item, spider):
        item['rating'] = float(item.get('rating').split(':')[-1][:-1])/10 if item.get('rating') is not None else None
        item['price'] = parsing_price(item)
        item['old_price'] = float(sub(r'[^\d,]','', item.get('old_price')).replace(',', '.')) if item.get('old_price') is not None else item.get('price')
        return item

    def parsing_price(item):
        price = item.get('price')
        searchObj = search(r'((\d+(?:[.,]\d{3})*)(?:[.,])(\d+))|\d+', price)
        if searchObj:
            if len(searchObj.groups()) == 1:
                parsed_price = searchObj.group()
            else:
                (num, inter, decimal) = searchObj.groups()
                inter = sub(r'[^\d]', '', inter)
                parsed_price =  inter + '.' + decimal
        else:
            raise DropItem(f"Missing price in {item}")
        return float(parsed_price)
