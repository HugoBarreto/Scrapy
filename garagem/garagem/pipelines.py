# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from re import sub, search

class LivroPipeline(object):

    def process_item(self, item, spider):
        item['rating'] = float(item.get('rating').split(':')[-1][:-1])/10 if item.get('rating', None) is not None else None
        item['price'] = self.parsing_price(item.get('price'), spider=spider)
        item['old_price'] = self.parsing_price(item.get('old_price'), spider=spider)

        if item.get('old_price'):
            item['discount'] = f"{(1 - item.get('price')/item.get('old_price')):.0%}" if item.get('old_price') > 0 else '0%'
        else:
            item['old_price'] = item.get('price')
            item['discount'] = '0%'

        return item

    def parsing_price(self, price, spider):
        '''
        parsing_price(str) -> float

        Takes any string represantition of a product's price and parses it to float

        'RS$ 100,58' -> 100.58 | 'US$ 1,400.58' -> 1400.58 | '1.100,00' -> 1100.00
        '''
        #This regex captures any price expression, check: https://regex101.com/r/mXbsGX/3
        searchObj = search(r'((\d+(?:[.,]\d{3})*)(?:[.,])(\d+))|\d+', price) if price is not None else None
        if searchObj:
            if searchObj.groups()[0] is None:
                parsed_price = searchObj.group()
            else:
                (num, inter, decimal) = searchObj.groups()
                inter = sub(r'[^\d]', '', inter)
                parsed_price =  inter + '.' + decimal if len(decimal) != 3 else inter + decimal
        else:
            parsed_price = None
            #raise DropItem(f"Missing price in {item}")
        return float(parsed_price) if parsed_price is not None else None
