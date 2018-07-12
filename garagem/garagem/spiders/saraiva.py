import scrapy


class SaraivaSpider(scrapy.Spider):
    name = "saraiva"
    start_urls = ['https://busca.saraiva.com.br/busca?q=intrinseca&page=1']


    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {'text': quote.css('span.text::text').extract_first(),
                    'author': quote.css('small.author::text').extract_first(),
                    'tags': quote.css('div.tags a.tag::text').extract(),}

        nextPage = response.xpath('//div[@class="neemu-pagination-container bottom"]//li[@class="neemu-pagination-next"]//@href').extract_first()
        if nextPage is not None:
            yield response.follow(nextPage, callback=self.parse)


        # if ".org" in response.url:
        #     from scrapy.shell import inspect_response
        #     inspect_response(response, self)
