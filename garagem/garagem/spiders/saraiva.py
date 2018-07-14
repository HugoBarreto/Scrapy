import scrapy
from scrapy_splash import SplashRequest
from garagem.items import Livro

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
        for product in products:
            product_info = product.css('div[class*="info"]')

            id = product.xpath('./@data-pid').extract_first()
            brand = product.xpath('./@data-brand').extract_first()
            title = product.xpath('./@data-name').extract_first()
            price = product.xpath('./@data-price').extract_first()
            old_price = product_info.css('span[class*="old-price"]::text').extract_first()
            author = product_info.css('div[class*="subtitle"]::text').extract_first()
            available = False if 'Produto indisponível' in product.xpath('.//text()').extract() else True
            url = product.xpath('./@data-produrl').extract_first()
            rating = product_info.xpath('.//div[@class="rating"]//@style').extract_first(default=None)
            evals = product_info.xpath('.//div[@class="rating"]/following-sibling::*/text()').re_first('\d+') if rating is not None else '0'

            book = Livro(id=id, brand=brand, title=title, price=price, old_price=old_price, author=author, available=available,
                rating=rating, evals=evals, url=url)

            yield book

        # Navegate through all pages related to the same brand
        nextPage = response.xpath('//div[@class="neemu-pagination-container bottom"]//li[@class="neemu-pagination-next"]//@href').extract_first()
        if nextPage is not None:
            yield response.follow(nextPage, callback=self.parse)
