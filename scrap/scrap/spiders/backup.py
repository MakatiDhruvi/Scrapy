import scrapy
from ..items import ScrapItem
# data that we bring and can store in form of html file

# class QuotesSpider(scrapy.Spider):
#     name = "spidername"

#     def start_requests(self):
#         urls = [
#             'https://quotes.toscrape.com/page/1/',
#             'https://quotes.toscrape.com/page/2/',
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = f'quotes-{page}.html'
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#         self.log(f'Saved file {filename}')



class QuoteSpider(scrapy.Spider):
    name = 'backup'
    page_number = 2
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):
        tablename = 'public.quotes'
        items = ScrapItem()

        all_div_quotes = response.css('div.quote')

        for quote in all_div_quotes:

            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

            yield items

        next_page = 'https://quotes.toscrape.com/page/' + str(QuoteSpider.page_number) + '/'
        if QuoteSpider.page_number < 11:
            QuoteSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
    