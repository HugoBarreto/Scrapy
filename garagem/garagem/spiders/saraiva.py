import scrapy
from scrapy_splash import SplashRequest
from re import sub, search
import re

class SaraivaSpider(scrapy.Spider):
    name = "saraiva"
    start_urls = ['https://busca.saraiva.com.br/busca?q=intrinseca&page=1',
        'https://busca.saraiva.com.br/busca?q=saraiva&page=1',
        'https://busca.saraiva.com.br/busca?q=sextante',
        'https://busca.saraiva.com.br/busca?q=companhia-das-letras',
        'https://busca.saraiva.com.br/busca?q=rocco',
        'https://busca.saraiva.com.br/busca?q=harpercollins',
        'https://busca.saraiva.com.br/busca?q=record',
        'https://busca.saraiva.com.br/busca?q=cia-das-letrinhas']

    #start_urls = ['https://busca.saraiva.com.br/busca?q=harpercollins&page=491'] #['https://busca.saraiva.com.br/pages/games/playstation-4/consoles']
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 0.5,})

    def parse(self, response):
        '''
        @url https://busca.saraiva.com.br/busca?q=intrinseca&page=1
        @scrapes id title brand price author url rating evals
        @returns requests 1 1
        @returns items 44
        '''
        products = response.css('ul[class*="neemu-products"]').xpath('li')
        # only_once = True
        for product in products:
            product_info = product.css('div[class*="info"]')
            rating = product_info.xpath('.//div[@class="rating"]//@style').extract_first(default=None)
            rating = rating.split(':')[-1] if rating is not None else rating
            evals = product_info.xpath('.//div[@class="rating"]/following-sibling::*/text()').re_first('\d+') if rating is not None else '0'
            price = product.xpath('./@data-price').extract_first()
            searchObj = search(r'((\d+(?:[.,]\d{3})*)(?:[.,])(\d+))|\d+', price)
            if searchObj:
                if searchObj.groups()[0] is None:
                    parsed_price = searchObj.group()
                else:
                    (num, inter, decimal) = searchObj.groups()
                    # print(f'inter type: {type(inter)}')
                    # print(f'num : {num}, inter : {inter}, decimal : {decimal}')
                    # print(f"id : {product.xpath('./@data-pid').extract_first()}")
                    inter = re.sub(r'[^\d]', '', inter)
                    parsed_price =  inter + '.' + decimal
            else:
                price = 'Missing'

            price = parsed_price
            #This regex captures any price expression, check: https://regex101.com/r/mXbsGX/2
            old_price = product_info.css('span[class*="old-price"]::text').re_first('\d+(?:[.,]\d+)*')
            # Dealing with brazillian prices (e.g. '2.499,00' -> '2499.00')
            old_price = sub(r'[^\d,]','', old_price).replace(',', '.') if old_price is not None else price
            try:
                discount = f'{(1 - float(price)/float(old_price)):.0%}' if float(old_price) > 0 else '0%'
            except:
                print(f'old_price : {old_price}')
                print(f'price : {price}')
            yield {
                    'id' : product.xpath('./@data-pid').extract_first(),
                    'brand' : product.xpath('./@data-brand').extract_first(),
                    'title' : product.xpath('./@data-name').extract_first(),
                    'price' : price,
                    'old_price' : old_price,
                    'discount' : discount,
                    'author' : product_info.css('div[class*="subtitle"]::text').extract_first(),
                    'available' : False if 'Produto indisponível' in product.xpath('.//text()').extract() else True,
                    'url' : product.xpath('./@data-produrl').extract_first(),
                    'rating' : rating,
                    'evals' : evals,
                  }
        # if response.url is not 'https://busca.saraiva.com.br/busca?q=harpercollins&page=619':
        #     yield response.follow('https://busca.saraiva.com.br/busca?q=harpercollins&page=492', callback=self.parse)
        nextPage = response.xpath('//div[@class="neemu-pagination-container bottom"]//li[@class="neemu-pagination-next"]//@href').extract_first()
        if nextPage is not None:
            yield response.follow(nextPage, callback=self.parse)
