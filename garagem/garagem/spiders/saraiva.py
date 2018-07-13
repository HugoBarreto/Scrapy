import scrapy
from scrapy_splash import SplashRequest

class SaraivaSpider(scrapy.Spider):
    name = "saraiva"
    start_urls = ['https://busca.saraiva.com.br/busca?q=intrinseca&page=1']

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url=url, callback=self.parse)

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
            rating = product_info.xpath('.//div[@class="rating"]//@style').extract_first(default='null').split(':')[-1]
            evals = product_info.xpath('.//div[@class="rating"]/following-sibling::*/text()').re_first('\d+') if rating is not 'null' else '0'
            yield {
                    'id' : product.xpath('./@data-pid').extract_first(),
                    'title' : product.xpath('./@data-name').extract_first(),
                    'brand' : product.xpath('./@data-brand').extract_first(),
                    'price' : product.xpath('./@data-price').extract_first(),
                    #old_price - Falta implementar
                    'author' : product_info.css('div[class*="subtitle"]::text').extract_first(),
                    'available' : 'false' if 'Produto indisponível' in product.xpath('.//text()').extract() else 'true',
                    'url' : product.xpath('./@data-prpdurl').extract_first(),
                    'rating' : rating,
                    'evals' : evals,
                  }

            # if (only_once) and (rating is 'null'):
            #     print('O que está acontecendo?')
            #     from scrapy.shell import inspect_response
            #     inspect_response(response, self)
            #     only_once = False

        nextPage = response.xpath('//div[@class="neemu-pagination-container bottom"]//li[@class="neemu-pagination-next"]//@href').extract_first()
        if nextPage is not None:
            yield response.follow(nextPage, callback=self.parse)


        # if ".org" in response.url:
        #     from scrapy.shell import inspect_response
        #     inspect_response(response, self)
